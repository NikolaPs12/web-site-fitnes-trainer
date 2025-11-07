from ..extensions import db
from datetime import datetime, time, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from ..models.users import User
import secrets

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.String(20), default='09:00') 

    # Данные клиента
    client_name = db.Column(db.String(50), nullable=False)
    client_email = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    
    # ✅ ИЗМЕНИТЬ: вместо имени тренера - связь с моделью Trener
    trener_id = db.Column(db.Integer, db.ForeignKey('trener.id'), nullable=False)
    
    status = db.Column(db.String(20), nullable=False, default='confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancel_token = db.Column(db.String(32), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.cancel_token:
            self.cancel_token = secrets.token_hex(16)

    

class WorkingHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.String(10), nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)

    __table_args__ = (
        CheckConstraint('open_time < close_time', name='check_open_before_close'),
    )



    
    