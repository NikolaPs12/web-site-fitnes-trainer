from sqlalchemy import CheckConstraint
from ..extensions import db
from datetime import time

class TrenerSchedule(db.Model):
    """Расписание работы тренеров по дням недели"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Связь с тренером
    trener_id = db.Column(db.Integer, db.ForeignKey('trener.id'), nullable=False)
    trener = db.relationship('Trener', backref=db.backref('schedules', lazy=True))
    
    # День недели (0-6, где 0=понедельник, 6=воскресенье)
    day_of_week = db.Column(db.Integer, nullable=False)  
    
    # Время начала и окончания работы
    start_time = db.Column(db.Time, nullable=False, default=time(9, 0))  # 09:00
    end_time = db.Column(db.Time, nullable=False, default=time(21, 0))   # 21:00
    
    # Активен ли этот день для записи
    is_working = db.Column(db.Boolean, default=True)
    
    __table_args__ = (
        CheckConstraint('day_of_week >= 0 AND day_of_week <= 6', name='check_day_range'),
        CheckConstraint('start_time < end_time', name='check_schedule_time'),
    )

class DayOff(db.Model):
    """Выходные дни и праздники тренеров"""
    id = db.Column(db.Integer, primary_key=True)
    
    trener_id = db.Column(db.Integer, db.ForeignKey('trener.id'), nullable=False)
    trener = db.relationship('Trener', backref=db.backref('days_off', lazy=True))
    
    # Дата выходного
    date = db.Column(db.Date, nullable=False, index=True)
    
    # Причина (отпуск, болезнь, праздник и т.д.)
    reason = db.Column(db.String(100), nullable=True)
    
    # Весь день выходной или частично
    is_full_day = db.Column(db.Boolean, default=True)
    
    # Если не полный день - указать время отсутствия
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)    