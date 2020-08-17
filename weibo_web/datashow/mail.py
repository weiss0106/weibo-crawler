# coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sendmail(receiver, mail_title, mail_body):
    # 收件人和发件人
    receiver = receiver
    sender = '348370619@qq.com'

    # 发件人邮箱的SMTP服务器（即sender的SMTP服务器）
    smtpserver = 'smtp.qq.com'

    # 发件人邮箱的用户名和授权码（不是登陆邮箱的密码）
    username = ''
    password = ''  # （83xxxx202@qq.com邮箱的授权码）

    mail_title = mail_title
    mail_body = mail_body

    # 创建一个实例
    message = MIMEText(mail_body, 'plain', 'utf-8')  # 邮件正文
    # (plain表示mail_body的内容直接显示，也可以用text，则mail_body的内容在正文中以文本的形式显示，需要下载）
    message['From'] = sender  # 邮件上显示的发件人
    message['To'] = receiver  # 邮件上显示的收件人
    message['Subject'] = Header(mail_title, 'utf-8')  # 邮件主题

    smtp = smtplib.SMTP()  # 创建一个连接
    smtp.connect(smtpserver)  # 连接发送邮件的服务器
    smtp.login(username, password)  # 登录服务器
    smtp.sendmail(sender, receiver, message.as_string())  # 填入邮件的相关信息并发送
    smtp.quit()
