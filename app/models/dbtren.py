from ..extensions import db
from datetime import datetime, time, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from .users import User
import secrets

class Trener(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    all_name = db.Column(db.String(60), nullable=False)
    avatar = db.Column(db.String(200), nullable=True, default=None)
    text = db.Column(db.Text, nullable=False)
    # ✅ Социальные сети
    instagram = db.Column(db.String(100), nullable=True)
    telegram = db.Column(db.String(100), nullable=True)
    vk = db.Column(db.String(100), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    
    # ✅ ДОБАВИТЬ ДЛЯ СИСТЕМЫ ЗАПИСИ:
    is_active = db.Column(db.Boolean, default=True)  # Активен ли тренер для записи
    specialization = db.Column(db.String(100), nullable=True)  # Специализация
    
    # Расписание работы тренера
    # список рабочих часов в масиве
    list_working_hours = db.Column(db.String(100), nullable=True) 
    
    # Связь с бронированиями
    bookings = db.relationship('Booking', backref='trener', lazy=True)

    def remove_time(self, time_to_remove):
        if not self.list_working_hours:
            return False

        time = [int(t) for t in self.list_working_hours.split(',') if t]
        if time_to_remove in time:
            time.remove(time_to_remove)
            self.list_working_hours = ','.join(time)
            db.session.commit()
            return True
        
        return False