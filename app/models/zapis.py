from ..extensions import db
from datetime import datetime, time, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
import secrets

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    # ✅ Исправлены имена для соответствия форме
    client_name = db.Column(db.String(50), nullable=False)
    client_email = db.Column(db.String(100), nullable=False)  # ✅ ДОБАВЛЕНО!
    client_phone = db.Column(db.String(20), nullable=False)
    
    trener_name = db.Column(db.String(50), nullable=False)

    status = db.Column(db.String(20), nullable=False, default='confirmed')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cancel_token = db.Column(db.String(32), unique=True, nullable=False)

    # user = db.relationship('User', backref=db.backref('bookings', lazy=True))  # ⚠️ Закомментируйте если нет модели User

    __table_args__ = (
        CheckConstraint('end_time > start_time', name='check_time_sequence'),
        CheckConstraint("status IN ('confirmed', 'cancelled', 'completed')", name='check_status'),
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Автогенерация cancel_token если не указан
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