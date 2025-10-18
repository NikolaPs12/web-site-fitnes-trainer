import os

from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://nikola:1234567890@localhost:5532/mydb" # Используем всю строку подключения целиком
    SECRET_KEY = os.environ.get('SECRET_KEY', '12345678')     # Лучше тоже хранить в переменной окружения
    SQLALCHEMY_TRACK_MODIFICATIONS = True               # Отключаем для производительности
