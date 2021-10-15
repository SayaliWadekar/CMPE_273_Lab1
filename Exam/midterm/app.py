from flask import Flask
from routes import twitter 


def create_app():
    app=Flask(__name__)
    app.register_blueprint(twitter)

    return app