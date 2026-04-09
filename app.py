from flask import Flask, request
from module import logs
import hmac
import hashlib
import subprocess

app = Flask(__name__)  # 初始化Flask
WEBHOOK_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 全局初始化日志记录对象
log = logs.configuration()

# 验证GitHub的签名
def verify_signature(payload, signature):
    secret = WEBHOOK_SECRET.encode('utf-8')
    computed_signature = hmac.new(secret, payload, hashlib.sha1).hexdigest()  # 计算签名
    return hmac.compare_digest(f'sha1={computed_signature}', signature)  # 比较签名


# 执行git pull命令拉取最新的代码
def gitPull():
    log.info(f'[pull]😊Start pulling the latest repository code.')
    try:
        # 进入/web目录并执行git pull
        result = subprocess.run(['git', 'pull', 'origin', 'main'], cwd='/web', capture_output=True, text=True)
        if result.returncode == 0:
            log.info(f'[pull]👌successfully Git pulling output: {result}')  # 记录正常输出日志
        else:
            log.warn(f'[pull]👋pulling the latest repository error, Output Logs is: {result}') # 记录错误输出日志
    except Exception as e:
        log.error(f'[pull]👋Exception occurred while running git pull: {e}')


# 重启 hexo 服务使配置文件生效
def hexoServer():
    log.info(f'[Hexo]😊Restart Hexo service, the modified configuration file takes effect.')
    try:
        # 执行systemctl restart hexo命令，重启hexo服务
        result = subprocess.run(['systemctl', 'restart', 'hexo'], capture_output=True, text=True)
        if result.returncode == 0:
            log.info(f'[Hexo]👌successfully restart Hexo Server output: {result}')  # 记录正常输出日志
        else:
            log.warn(f'[Hexo]👋Restart Hexo Server error, Output Logs is: {result}')  # 记录错误输出日志
    except Exception as e:
        log.error(f'[Hexo]👋 Command execution error, Output Logs is:{e}')


# 获取请求IP地址
def get_client_ip(request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]  # 返回第一个 IP 地址，即客户端的真实 IP
    else:
        return request.headers.get('X-Real-IP', request.remote_addr)  # 如果没有 X-Forwarded-For，可能直接从请求中获取 IP


@app.route("/", methods=['post'])
@app.route("/webhook", methods=['post'])
def webhook():
    ip_address = get_client_ip(request)
    payload = request.get_data()
    signature = request.headers.get('X-Hub-Signature')

    if not signature:
        log.error(f'[login]👋IP: {ip_address} - Signature Error')
        return 'Signature Error', 400

    elif not verify_signature(payload, signature):
        log.error(f'[login]👋IP: {ip_address} - Signature Error')
        return 'Signature Error', 400

    elif verify_signature(payload, signature):
        log.info(f'[login]👌IP: {ip_address} - Webhook event received and verified successfully.')
        gitPull()    # 执行git pull
        hexoServer() # 重启 hexo 服务
        return 'Signature successful', 200

if __name__ == "__main__":
    app.run(port=5050, host="0.0.0.0")
