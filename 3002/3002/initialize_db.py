# initialize_db.py
from app import db, app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes
        db.create_all()

    return app