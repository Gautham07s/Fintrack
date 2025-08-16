import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-prod")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///fintrack.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
