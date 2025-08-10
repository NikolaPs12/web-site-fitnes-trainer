import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Используем всю строку подключения целиком
    SECRET_KEY = os.environ.get('SECRET_KEY', '12345678')     # Лучше тоже хранить в переменной окружения
    SQLALCHEMY_TRACK_MODIFICATIONS = False                    # Отключаем для производительности
