import os
import random
import string

from captcha.image import ImageCaptcha
from flask import jsonify, request, session, make_response
from flask_mail import Message

from database import db
from mail import mail
from . import auth
from .models import Users


@auth.route('/varify/<string:username>&<string:email>')
def varify(username, email):
    # 生成一个6位数的验证码
    verification_code = str(random.randint(100000, 999999))
    session.permanent = True
    session['verification_code'] = verification_code
    print(session)
    # 创建邮件消息
    msg = Message('【妙笔】用户注册邮箱验证', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
    msg.body = ('Hi，【{}】：\n\n您正尝试通过本邮箱接收注册【妙笔】时所需的验证码。\n\n'
                '验证码：【{}】，5分钟内有效，如非本人操作，请忽略本邮件。').format(username, verification_code)
    # 发送邮件
    mail.send(msg)
    return jsonify({'message': '验证码已发送，请注意查收！', 'code': 200})


@auth.route('/captcha')
def captcha():
    # 生成随机的验证码
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    # 将验证码存储到 session 中
    session['captcha'] = captcha_text
    print(session)
    # 生成验证码图片
    image = ImageCaptcha()
    image_data = image.generate(captcha_text)
    # 创建响应对象并设置响应头，以便浏览器将其作为图片处理
    response = make_response(image_data.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(session)
    # 验证验证码
    if 'verification_code' not in session or data['verification_code'] != session['verification_code']:
        return jsonify({'message': '验证码错误或已失效！', 'code': 400})
    # 验证邮箱是否已被注册
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'message': '邮箱已被注册！', 'code': 400})
    # 注册新用户
    new_user = Users(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '用户注册成功！', 'code': 200})


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(session)
    # 验证验证码
    if 'captcha' not in session or data['captcha'].upper() != session['captcha']:
        return jsonify({'message': '验证码错误！', 'code': 400})
    # 验证用户是否存在
    user = Users.query.filter_by(email=data['email']).first()
    if user is None:
        return jsonify({'message': '邮箱未注册！', 'code': 400})
    # 验证密码是否正确
    if not user.check_password(data['password']):
        return jsonify({'message': '密码错误！', 'code': 400})
    session['user_id'] = user.id
    return jsonify({'message': '用户登录成功！', 'code': 200})
