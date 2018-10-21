from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from app import app

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('武院LAF服务器 <%s>' % sender_user)
    msg['To'] = _format_addr('管理员 <%s>' % to_addr)
    msg['Subject'] = Header('LAF用户反馈', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(sender_user, sender_pwd)
    server.sendmail(sender_user, [to_addr], msg.as_string())
    server.quit()

sender_user = 'k_1043@126.com'
sender_pwd = app.config['EMAIL_PWD']
to_addr = 'k_1043@126.com'
smtp_server = 'smtp.126.com'
