from flask_mail import Message

from mail import mail
from . import main


@main.route('/')
def index():
    msg = Message('【妙笔】用户注册邮箱验证', sender='2234333815@qq.com', recipients=['2234333815@qq.com'])
    msg.body = msg.body = 'Hi，【Admin】：\n\n您正尝试通过本邮箱接收注册【妙笔】时所需的验证码。\n\n验证码：908997，5分钟内有效，如非本人操作，请忽略本邮件。'

    mail.send(msg)
    return 'Email has been sent!'
