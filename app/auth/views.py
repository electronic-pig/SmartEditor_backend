import random
import string

from captcha.image import ImageCaptcha
from flask import jsonify, request, session, make_response

from database import db
from . import auth
from .models import Users


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
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'message': '邮箱已被注册！', 'code': 400})
    new_user = Users(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '用户注册成功！', 'code': 201})


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(session)
    if 'captcha' not in data or data['captcha'].upper() != session.get('captcha', ''):
        return jsonify({'message': '验证码错误！', 'code': 400})
    user = Users.query.filter_by(email=data['email']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'message': '邮箱或密码错误！', 'code': 400})
    session['user_id'] = user.id
    return jsonify({'message': '用户登录成功！', 'code': 200})
