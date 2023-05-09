from db import session_info
import json
from nicegui import ui
import smtplib
from email.mime.text import MIMEText
from email.header import Header

SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SMTP_USER = "13921008716@163.com"
SMTP_PASSWORD = "PVARTJHWBBKRVTWI"


def is_authenticated(session_id) -> bool:
    return session_info.get(session_id, {}).get("authenticated", False)


async def set_item(key, data):
    if not isinstance(data, str):
        data = json.dumps(data)
    await ui.run_javascript(
        f"""
    window.localStorage.setItem('{key}', `{data}`)
    """,
        respond=False,
    )


async def get_item(key):
    result = await ui.run_javascript(
        f"""
    window.localStorage.getItem('{key}')
    """
    )
    try:
        return json.loads(result)
    except:
        return result


def send_email(to_addr, subject, content):
    """
    使用163邮箱发送电子邮件

    :param to_addr: 收件人地址，字符串类型
    :param subject: 邮件主题，字符串类型
    :param content: 邮件内容，字符串类型
    :return: 发送成功返回True，否则返回False
    """
    try:
        # 创建SMTP连接
        smtp_obj = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

        # 登录邮箱
        smtp_obj.login(SMTP_USER, SMTP_PASSWORD)

        # 创建邮件对象
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = SMTP_USER
        msg["To"] = to_addr
        msg["Subject"] = Header(subject, "utf-8")

        # 发送邮件
        smtp_obj.sendmail(SMTP_USER, to_addr, msg.as_string())

        # 关闭SMTP连接
        smtp_obj.quit()

        # 发送成功
        return True
    except Exception as e:
        # 发送失败
        print(e)
        return False
