from flask import Flask
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from database import db


def create_app():
    app = Flask(__name__)
    app.secret_key = 'my secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aliserver@47.236.92.108:3306/smart_editor'

    db.init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
