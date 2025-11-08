from flask import Flask, render_template, request, redirect, Request, Blueprint, url_for, flash, session
from ..extensions import db, login_manager, migrate, socketio
from ..forms import SimpleBookingForm
from ..models.zapis import Booking
from ..models.dbtren import Trener
from ..models.users import User
from flask import current_app as app
from datetime import datetime, timedelta
from ..functions import admin_required
from flask_login import current_user, login_required
from flask_socketio import emit
import secrets

zapis = Blueprint('zapis', __name__)

@zapis.route('/appoint', methods=['GET', 'POST'])
def zap():
    form = SimpleBookingForm()
    
    if form.validate_on_submit():
        # ✅ ИСПРАВЛЕНО: QuerySelectField возвращает объект Trener, а не имя
        trener = form.trener_name.data  # Это объект Trener, а не строка!
        print(f"🔍 DEBUG: Selected trener = {trener}")
        if not trener:
            flash('Тренер не найден.', 'danger')
            return render_template('book/booking.html', form=form)
            
        trener_id = trener.id  # Получаем ID из объекта
        trener_name = trener.all_name  # Получаем имя для отладки

        time_slot = form.time_slot.data
        print(f"🔍 DEBUG: time_slot from form = {repr(time_slot)}")
        print(f"🔍 DEBUG: trener object = {trener}")
        print(f"🔍 DEBUG: trener_id = {trener_id}")
        print(f"🔍 DEBUG: trener_name = {trener_name}")

        if not time_slot:
            flash('Выберите время', 'danger')
            return render_template('book/booking.html', form=form)
    
        # Проверка доступности слота
        existing_booking = Booking.query.filter_by(
            trener_id=trener_id,
            booking_date=form.booking_date.data,
            time=time_slot
        ).first()
        print(f"🔍 DEBUG: existing_booking = {existing_booking}")
        if existing_booking:
            flash('Это время уже забронировано. Пожалуйста, выберите другое.', 'danger')
            return render_template('book/booking.html', form=form)
        
        # Создание новой брони
        new_booking = Booking(
            client_name=form.client_name.data,
            client_email=form.client_email.data,
            client_phone=form.client_phone.data,
            trener_id=trener_id,
            booking_date=form.booking_date.data,
            time=time_slot,
            cancel_token=secrets.token_hex(16)
        )
        print(f"🔍 DEBUG: new_booking = {new_booking}")
        try:
            db.session.add(new_booking)
            db.session.commit()
            flash('Бронирование успешно создано!', 'success')
            
            socketio.emit('time_slot_removed', {
                'trener_id': trener_id,
                'time_slot': time_slot,
                'date': form.booking_date.data.strftime('%Y-%m-%d')
            }, namespace="/booking", broadcast=True)
            
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании бронирования. Пожалуйста, попробуйте снова.', 'danger')
            app.logger.error(f'Бронирование ошибка: {str(e)}')
    
    else:
        # ✅ ДЕБАГ: если форма не прошла валидацию
        print(f"🔍 DEBUG: Form validation failed. Errors: {form.errors}")
        if form.trener_name.errors:
            print(f"🔍 DEBUG: Trener field errors: {form.trener_name.errors}")
    
    return render_template('book/booking.html', form=form)

@zapis.route('/test-flash')
def test_flash():
    flash('✅ Тестовое успешное сообщение!', 'success')
    flash('⚠️ Тестовое предупреждение!', 'warning')
    flash('❌ Тестовое сообщение об ошибке!', 'danger')
    return redirect(url_for('zapis.zap'))

@zapis.route('/all_bookings', methods=['GET'])
@admin_required
@login_required
def all_bookings():    
    user_role = session.get('user_role')
    
    if user_role == "trener" and current_user.name == Trener.query.filter_by(current_user.name).first().all_name:
        user_id = session.get('user_id')
        trener = Trener.query.filter_by(user_id=user_id).first()
        bookings = Booking.query.filter_by(trener_id=trener.id)\
            .order_by(Booking.booking_date.desc(), Booking.time.desc())\
            .all()
    else:
        bookings = Booking.query.order_by(Booking.booking_date.desc(), Booking.time.desc()).all()
        trener = None
    return render_template('book/all_bookings.html', bookings=bookings, trener=trener)