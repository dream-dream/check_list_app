import redis
import pymysql
from datetime import timedelta
from DBUtils.PooledDB import PooledDB, SharedDBConnection
import mongoengine


class Config():
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    # DATABASE_URL = MONGO_URL = 'mongodb://username:passwd@localhost:27017/test'
    SESSION_REDIS = redis.Redis(host="localhost", port=6379)


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS_CON = redis.ConnectionPool(host="localhost", port=6379)
    REDIS_OBJ = redis.Redis(connection_pool=REDIS_CON)


class TestingConfig(Config):
    TESTING = True
