from dataclasses import field
from wtforms import StringField, PasswordField, validators, DateField, SubmitField, BooleanField, SelectField   
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from .models.users import User
from datetime import date, timedelta
from .models.zapis import Booking, WorkingHours


class SimpleBookingForm(FlaskForm):
    # Поля клиента
    client_name = StringField('ФИО*', validators=[
        DataRequired(message="Обязательное поле"),
        Length(min=2, max=100, message="Имя должно быть от 2 до 100 символов")
    ])
    
    trener_name = StringField('Имя тренера*', validators=[
        DataRequired(message="Обязательное поле"), 
        Length(min=2, max=50, message="Имя тренера должно быть от 2 до 50 символов")
    ])

    client_email = StringField('Email*', validators=[
        DataRequired(message="Обязательное поле"),
        Email(message="Введите корректный email")
    ])
    
    client_phone = StringField('Телефон*', validators=[
        DataRequired(message="Обязательное поле"),
        Length(min=7, max=20, message="Некорректный номер телефона")
    ])
    
    # Дата бронирования
    booking_date = DateField('Дата*', validators=[
        DataRequired(message="Выберите дату")
    ], format='%Y-%m-%d')
    
    # Время бронирования (выпадающий список)
    time_slot = SelectField('Время*', choices=[
            ('09:00', '09:00 - 10:00'),
            ('10:00', '10:00 - 11:00'),
            ('11:00', '11:00 - 12:00'),
            ('12:00', '12:00 - 13:00'),
            ('13:00', '13:00 - 14:00'),
            ('14:00', '14:00 - 15:00'),
            ('15:00', '15:00 - 16:00'),
            ('16:00', '16:00 - 17:00'),
            ('17:00', '17:00 - 18:00')
        ], validators=[
        DataRequired(message="Выберите время")
    ])
    
    submit = SubmitField('Забронировать')

    def validate_booking_date(self, field):  # ✅ Исправлен параметр
        if field.data < date.today():
            raise ValidationError("Дата бронирования не может быть в прошлом.")
        if field.data > date.today() + timedelta(days=30):
            raise ValidationError("Дата бронирования не может быть более чем на 30 дней вперед.")
        
        if field.data.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            raise ValidationError("Бронирование на выходные дни недоступно.")

    def validate_time_slot(self, field):  # ✅ Исправлен параметр
        if not field.data:
            raise ValidationError("Пожалуйста, выберите время бронирования.")
        
        if field.data not in [choice[0] for choice in self.time_slot.choices]:
            raise ValidationError("Выбранное время недоступно. Пожалуйста, выберите другое время.")

    def validate_client_phone(self, field):  # ✅ Исправлен параметр и логика
        phone = field.data
        # Более гибкая проверка телефона
        cleaned_phone = ''.join(filter(str.isdigit, phone))  # Оставляем только цифры
        
        if len(cleaned_phone) < 7 or len(cleaned_phone) > 15:
            raise ValidationError("Некорректный номер телефона.")

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[Length(max=20)])
    submit = SubmitField('Register')  

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    phone = StringField('Phone', validators=[Length(max=20)])
    submit = SubmitField('Login')      