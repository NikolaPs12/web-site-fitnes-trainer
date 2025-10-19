from flask import Flask, render_template, request, redirect, Request, Blueprint, url_for, flash
from ..extensions import db, login_manager, migrate
from ..forms import SimpleBookingForm
from ..models.zapis import Booking
from flask import current_app as app
from datetime import datetime, timedelta
import secrets

zapis = Blueprint('zapis', __name__)

@zapis.route('/appoint', methods=['GET', 'POST'])
def zap():
    form = SimpleBookingForm()
    
    if form.validate_on_submit():
        # Преобразуем строку времени в объект time
        start_time = datetime.strptime(form.time_slot.data, '%H:%M').time()
        
        # ✅ ПРАВИЛЬНАЯ проверка доступности слота
        existing_booking = Booking.query.filter_by(
            booking_date=form.booking_date.data,  # ✅ Правильное имя поля
            start_time=start_time                 # ✅ Правильное имя поля
        ).first()
        
        if existing_booking:
            flash('Это время уже забронировано. Пожалуйста, выберите другое.', 'danger')
            return render_template('book/booking.html', form=form)
        
        # Вычисляем end_time (start_time + 1 час)
        start_datetime = datetime.combine(form.booking_date.data, start_time)
        end_datetime = start_datetime + timedelta(hours=1)
        
        # ✅ ПРАВИЛЬНОЕ создание новой брони
        new_booking = Booking(
            client_name=form.client_name.data,      # ✅ Правильное имя
            client_email=form.client_email.data,    # ✅ Нужно добавить в модель!
            client_phone=form.client_phone.data,    # ✅ Правильное имя
            trener_name=form.trener_name.data,      # ✅ Правильное имя
            booking_date=form.booking_date.data,    # ✅ Правильное имя
            start_time=start_time,                  # ✅ Правильное имя
            end_time=end_datetime.time(),           # ✅ Правильное имя
            cancel_token=secrets.token_hex(16)      # ✅ Добавляем токен
        )
        
        try:
            db.session.add(new_booking)
            db.session.commit()
            flash('Бронирование успешно создано!', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании бронирования. Пожалуйста, попробуйте снова.', 'danger')
            app.logger.error(f'Бронирование ошибка: {str(e)}')
    
    return render_template('book/booking.html', form=form)  # ✅ Исправлен путь к шаблону

@zapis.route('/test-flash')
def test_flash():
    flash('✅ Тестовое успешное сообщение!', 'success')
    flash('⚠️ Тестовое предупреждение!', 'warning')
    flash('❌ Тестовое сообщение об ошибке!', 'danger')
    return redirect(url_for('zapis.zap'))