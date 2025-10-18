import psycopg2
from sqlalchemy import create_engine, text

def test_postgres():
    print("Тестируем подключение к PostgreSQL на порту 5532...")
    
    # Параметры подключения
    db_params = {
        'host': 'localhost',
        'port': 5532,
        'database': 'mydb', 
        'user': 'nikola',
        'password': '1234567890'
    }
    
    # Тест 1: Прямое подключение psycopg2
    try:
        conn = psycopg2.connect(**db_params)
        print("✓ Psycopg2 подключение: УСПЕХ")
        
        # Проверим список таблиц
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cur.fetchall()
        print(f"  Таблицы в базе: {[t[0] for t in tables]}")
        
        conn.close()
    except Exception as e:
        print(f"✗ Psycopg2 ошибка: {e}")
        return False
    
    # Тест 2: SQLAlchemy подключение
    try:
        engine = create_engine("postgresql://nikola:1234567890@localhost:5532/mydb")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), current_user"))
            db_info = result.fetchone()
            print(f"✓ SQLAlchemy подключение: УСПЕХ")
            print(f"  База: {db_info[0]}, Пользователь: {db_info[1]}")
        return True
    except Exception as e:
        print(f"✗ SQLAlchemy ошибка: {e}")
        return False

if __name__ == "__main__":
    test_postgres()