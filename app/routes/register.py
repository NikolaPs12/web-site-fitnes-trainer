from flask import Blueprint, render_template, redirect, url_for, flash

from app.forms import RegistrationForm
from ..models.users import User
from ..extensions import db
from werkzeug.security import generate_password_hash


register_bp = Blueprint('register', __name__)

@register_bp.route('/registr', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(name=form.name.data,
                        email=form.email.data,
                        password=hashed_password,
                        phone=form.phone.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Aккаунт успешно создан!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка во время регистрации. Пожалуйста повторите попытку.', 'danger')
    return render_template('user/reg.html', form=form)        