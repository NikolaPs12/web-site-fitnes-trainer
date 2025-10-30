from app import create_app 
from dotenv import load_dotenv
from app.extensions import socketio
import os

# Загружаем переменные окружения
load_dotenv()

# Создаем приложение
app = create_app()

if __name__ == '__main__':
    print("🚀 Запускаем сервер...")
    socketio.run(app, debug=True)