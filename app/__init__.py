import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from database import db
from mail import mail
from .auth import auth as auth_blueprint
from .document import document as document_blueprint


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  # 允许跨域请求

    load_dotenv()  # 加载 .env 文件(存储敏感信息)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['MAIL_SERVER'] = 'smtp.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    db.init_app(app)  # 创建数据库连接
    mail.init_app(app)  # 创建邮件客户端连接

    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # 注册蓝图
    app.register_blueprint(document_blueprint, url_prefix='/document')  # 注册蓝图

    return app
