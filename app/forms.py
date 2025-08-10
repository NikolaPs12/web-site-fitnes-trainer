from wtforms import StringField, PasswordField, validators, FileField, SubmitField, BooleanField, SelectField   
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed

class ZapisForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last_Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')