# database.py
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
redis_client = FlaskRedis(decode_responses=True)
