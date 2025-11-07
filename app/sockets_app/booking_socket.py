from flask_socketio import emit
from flask import request
from ..extensions import socketio, db
from ..models.dbtren import Trener
from ..models.zapis import Booking
from ..forms import SimpleBookingForm
from datetime import datetime
def init_socket_booking(socketio):
    @socketio.on('connect', namespace="/booking")
    def handle_connect():
        print(f"✅ Клиент подключился: {request.sid}")
        

    @socketio.on('disconnect', namespace="/booking")
    def handle_disconnect():
        print(f"❌ Клиент отключился: {request.sid}")

    @socketio.on('get_slots', namespace="/booking")
    def handle_get_slots(data):
        print("🎯 Получен запрос get_slots:", data)
        trener_id = data.get('trener_id')

        trener = Trener.query.get(trener_id)
        if not trener:
            emit("slots_response", {"error": "Тренер не найден"})
            return
        
        if trener.list_working_hours:
            clean_hours = trener.list_working_hours.replace('{', '').replace('}', '')
            slots = [time.strip() for time in clean_hours.split(',') if time.strip()]
        else:
            slots = []
        print(f"📤 Отправка слотов для тренера {trener_id}: {slots}")
        

        emit("slots_response", {"slots": slots, "trener_id": trener_id})


    @socketio.on("view_booking", namespace="/booking")
    def handle_view_booking(data):
        print("👀 Получен запрос view_booking:", data)
        trener_id = data.get('trener_id')
        booking_date = data.get('booking_date')

        trener = Trener.query.get(trener_id)
        if not trener:
            emit("booking_response", {"error": "Тренер не найден"})
            return
        
        works_hours = trener.list_working_hours
        if works_hours:
            clean_hours = works_hours.replace('{', '').replace('}', '')
            all_slots = [time.strip() for time in clean_hours.split(',') if time.strip()]
        else:
            all_slots = []

        print(f"📋 Все рабочие слоты тренера: {all_slots}")

        bookings = Booking.query.filter_by(
            trener_id=trener_id,
            booking_date=datetime.strptime(booking_date, '%Y-%m-%d').date()
        ).all()

        booked_slots = [booking.start_time.strftime('%H:%M') for booking in bookings]
        print(f"📅 Занятые слоты на {booking_date}: {booked_slots}")

        # ✅ ИСПРАВЛЕННАЯ ФИЛЬТРАЦИЯ:
        available_slots = []
        for slot_range in all_slots:
            # Извлекаем начало диапазона (например, из "14:00-15:00" берем "14:00")
            slot_start = slot_range.split('-')[0].strip()
            
            # Если начало слота НЕ в занятых, то слот доступен
            if slot_start not in booked_slots:
                available_slots.append(slot_range)

        print(f"✅ Доступные слоты после фильтрации: {available_slots}")

        emit("booking_response", {"available_slots": available_slots, "trener_id": trener_id, "booking_date": booking_date})