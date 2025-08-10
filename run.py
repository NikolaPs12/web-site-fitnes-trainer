from app import create_app
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

# Создаем приложение
application = create_app()

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=8080) 
    