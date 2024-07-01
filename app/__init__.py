import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from database import *
from mail import mail
from .auth import auth as auth_blueprint
from .document import document as document_blueprint
from .function import function as function_blueprint


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  # 允许跨域请求

    load_dotenv()  # 加载 .env 文件(存储敏感信息)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # 设置ACCESS_TOKEN的永不过期
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['REDIS_URL'] = os.getenv('REDIS_DATABASE_URI')
    app.config['MAIL_SERVER'] = 'smtp.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    db.init_app(app)  # 创建mysql连接
    redis_client.init_app(app)  # 创建 Redis 连接
    mail.init_app(app)  # 创建邮件客户端连接
    JWTManager(app)  # 创建 JWTManager 实例

    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # 注册蓝图
    app.register_blueprint(document_blueprint, url_prefix='/document')  # 注册蓝图
    app.register_blueprint(function_blueprint, url_prefix='/function')  # 注册蓝图

    return app
