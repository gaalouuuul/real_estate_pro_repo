import redis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cache = redis.Redis(host="localhost", port=6379, decode_responses=True)