# config.py
from app import create_app


app = create_app()

if __name__ == '__main__':
    app.run()

    
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movies.db'

# config.py

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_test_secret_key'
