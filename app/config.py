import os

class Config(object):
    # Получаем значения из переменных окружения или используем значения по умолчанию
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'nikola')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'mydatabase')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5632')
    
    # Форматируем строку подключения
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    
    SECRET_KEY = '12345678'
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # Лучше отключить для производительности