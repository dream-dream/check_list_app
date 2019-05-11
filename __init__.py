import os, sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from mongoengine import *
from flask_mongoengine import MongoEngine
from flask_cors import CORS

from .loggins import LoggingSet
db = MongoEngine()
logger = LoggingSet()


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings.DevelopmentConfig")
    app.config['MONGODB_SETTINGS'] = {
        'db': 'test',
        'host': 'localhost',
        'port': 27017,
    }
    logger.debug_log(logging.DEBUG)
    logger.error_log(logging.ERROR)
    db.init_app(app)
    app.debug = True
    return app


app = create_app()
CORS(app, resources=r'/*')


def register_blueprints(app):
    from .views.view import api
    app.register_blueprint(api, url_prefix='/api/v1')


register_blueprints(app)
# app.register_blueprint(api, url_prefix='/api/v1')
