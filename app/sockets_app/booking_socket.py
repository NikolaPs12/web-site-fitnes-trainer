from flask_socketio import emit
from flask import request
from ..extensions import socketio, db
from ..models.dbtren import Trener

def init_socket_booking(socketio):
    @socketio.on('connect', namespace="/booking")
    def handle_connect():
        print(f"✅ Клиент подключился: {request.sid}")
        
        # Автоматически отправляем тестовые слоты при подключении
        test_slots = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"]
        emit('slots_response', {"slots": test_slots})
        print(f"📤 Отправлены тестовые слоты: {test_slots}")

    @socketio.on('disconnect', namespace="/booking")
    def handle_disconnect():
        print(f"❌ Клиент отключился: {request.sid}")

    @socketio.on('get_slots', namespace="/booking")
    def handle_get_slots(data):
        print("🎯 Получен запрос get_slots:", data)
        
        date = data.get('date')
        trener_id = data.get('trener_id')
        
        print(f"📅 Дата: {date}, Тренер ID: {trener_id}")
        
        # Тестовые данные - можно заменить на реальные из БД
        test_slots = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"]
        
        print(f"📤 Отправляю слоты: {test_slots}")
        emit("slots_response", {"slots": test_slots})

    # ... остальные обработчики ...