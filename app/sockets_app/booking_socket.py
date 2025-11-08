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

    from flask_socketio import emit
from flask import request
from ..extensions import socketio, db
from ..models.dbtren import Trener
from ..models.zapis import Booking
from datetime import datetime

def init_socket_booking(socketio):
    @socketio.on('connect', namespace="/booking")
    def handle_connect():
        print(f"✅ Клиент подключился: {request.sid}")
        
    @socketio.on('disconnect', namespace="/booking")
    def handle_disconnect():
        print(f"❌ Клиент отключился: {request.sid}")

    @socketio.on('get_available_slots', namespace="/booking")
    def handle_get_available_slots(data):
        print("🎯 Получен запрос get_available_slots:", data)
        
        # 1. Получаем данные от пользователя
        trener_id = data.get('trener_id')
        booking_date = data.get('booking_date')  # Дата которую выбрал пользователь
        
        print(f"📅 Пользователь выбрал дату: {booking_date}")
        print(f"👨‍🏫 Пользователь выбрал тренера ID: {trener_id}")

        # 2. Проверяем тренера
        if not trener_id:
            print("⚠️ Не выбран тренер")
            emit("available_slots_response", {"error": "Не выбран тренер", "slots": []})
            return

        try:
            trener_id = int(trener_id)
        except (ValueError, TypeError):
            print("⚠️ Неверный формат trener_id")
            emit("available_slots_response", {"error": "Неверный ID тренера", "slots": []})
            return

        trener = Trener.query.get(trener_id)
        if not trener:
            print("⚠️ Тренер не найден")
            emit("available_slots_response", {"error": "Тренер не найден", "slots": []})
            return

        # 3. Получаем ВСЕ рабочие часы тренера
        if trener.list_working_hours:
            clean_hours = trener.list_working_hours.replace('{', '').replace('}', '')
            all_working_slots = [time.strip() for time in clean_hours.split(',') if time.strip()]
        else:
            all_working_slots = []

        print(f"📋 Все рабочие слоты тренера '{trener.all_name}': {all_working_slots}")

        # 4. Если дата не выбрана - показываем все рабочие слоты
        if not booking_date:
            print("📤 Отправляем ВСЕ рабочие слоты (дата не выбрана)")
            emit("available_slots_response", {
                "slots": all_working_slots, 
                "trener_id": trener_id,
                "message": "Выберите дату чтобы увидеть доступное время"
            })
            return

        # 5. Если дата выбрана - фильтруем занятые слоты
        try:
            # Преобразуем строку даты в объект date
            selected_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
            print(f"🔍 Ищем брони на дату: {selected_date}")
            
            # Ищем ВСЕ бронирования этого тренера на выбранную дату
            bookings_on_date = Booking.query.filter_by(
                trener_id=trener_id,
                booking_date=selected_date
            ).all()

            print(f"📊 Найдено бронирований на {selected_date}: {len(bookings_on_date)}")
            
            # Получаем список занятых слотов
            booked_slots = [booking.time for booking in bookings_on_date]
            print(f"🚫 Занятые слоты: {booked_slots}")

            # 6. ФИЛЬТРУЕМ: оставляем только свободные слоты
            available_slots = []
            for slot in all_working_slots:
                if slot not in booked_slots:
                    available_slots.append(slot)

            print(f"✅ Свободные слоты после фильтрации: {available_slots}")
            print(f"📈 Статистика: всего {len(all_working_slots)} рабочих, занято {len(booked_slots)}, свободно {len(available_slots)}")

            # 7. Отправляем результат на фронтенд
            emit("available_slots_response", {
                "slots": available_slots,
                "trener_id": trener_id,
                "booking_date": booking_date,
                "stats": {
                    "total_working": len(all_working_slots),
                    "booked": len(booked_slots),
                    "available": len(available_slots)
                }
            })
            
        except Exception as e:
            print(f"❌ Ошибка при обработке даты: {e}")
            emit("available_slots_response", {
                "error": f"Ошибка при загрузке слотов: {str(e)}", 
                "slots": []
            })