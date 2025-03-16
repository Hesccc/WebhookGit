# WebhookGit

使用Python Flask模块创建Webhook服务，监听Github repository push更新通知事件。当webhook服务监听到有githubb 发过来的push更新事件时，在服务器上执行git pull命令拉取最新的仓库。
()[https://ovvo.oss-cn-shenzhen.aliyuncs.com/Hexo_CICDFlowChart.png]

# 使用systemctl管理webhook
使用systemctl来管理hexo服务,创建/usr/lib/systemd/system/hexo-webhook.service配置文件并添加以下配置。创建完成后启动服务和设置开机启动

> 启动服务: systemctl start hexo-webhook
>
> 查看状态: systemctl status hexo-webhook
>
> 停止服务: systemctl stop hexo-webhook
>
> 设置开机启动: systemctl enable hexo-webhook
> 
> 禁用开机启动: systemctl disable hexo-webhook
