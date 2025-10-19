# test_db.py
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.users import User

def test_database():
    app = create_app()
    
    with app.app_context():
        print("🔍 Тестируем подключение к базе данных...")
        
        try:
            # Проверяем подключение
            db.session.execute('SELECT 1')
            print("✅ Подключение к базе данных успешно!")
            
            # Пробуем добавить тестового пользователя
            print("🔄 Добавляем тестового пользователя...")
            test_user = User(
                name="Test User",
                email="test@example.com", 
                password="testpassword123",
                phone="1234567890"
            )
            
            db.session.add(test_user)
            db.session.commit()
            print("✅ Тестовый пользователь успешно добавлен в базу данных!")
            
            # Пробуем выбрать добавленного пользователя
            print("🔍 Ищем пользователя в базе данных...")
            user_from_db = User.query.filter_by(email="test@example.com").first()
            
            if user_from_db:
                print(f"✅ Пользователь найден в базе данных:")
                print(f"   ID: {user_from_db.id}")
                print(f"   Имя: {user_from_db.name}")
                print(f"   Email: {user_from_db.email}")
                print(f"   Телефон: {user_from_db.phone}")
            else:
                print("❌ Пользователь не найден в базе данных!")
                
        except Exception as e:
            print(f"❌ Ошибка при работе с базой данных: {str(e)}")
            db.session.rollback()
        
        # Проверяем общее количество пользователей
        try:
            user_count = User.query.count()
            print(f"📊 Всего пользователей в базе: {user_count}")
        except Exception as e:
            print(f"❌ Ошибка при подсчете пользователей: {str(e)}")

if __name__ == "__main__":
    test_database()