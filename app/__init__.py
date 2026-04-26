from flask import Flask
from .extensions import db
from config import Config

def create_app():
    app = Flask(__name__)

    
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return "Hello"

    return app