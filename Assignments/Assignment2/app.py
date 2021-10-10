from flask import Flask
from routes import bitly 


def create_app(config_file='settings.py'):
    app=Flask(__name__)
    app.register_blueprint(bitly)

    return app