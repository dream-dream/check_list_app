import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from mongoengine import *
from flask_mongoengine import MongoEngine
from flask_script import Manager, Server

db = MongoEngine()


def create_app():
    app = Flask(__name__)
    connect('test', host='127.0.0.1', port=27017)
    app.config.from_object("settings.DevelopmentConfig")
    app.config['MONGODB_SETTINGS'] = {
        'db': 'test',
        'host': 'localhost',
        'port': 27017
    }
    db.init_app(app)
    app.debug = True
    return app


app = create_app()


def register_blueprints(app):
    from flask_check_list.views.view import api
    app.register_blueprint(api, url_prefix='/api/v1')


register_blueprints(app)
# app.register_blueprint(api, url_prefix='/api/v1')
