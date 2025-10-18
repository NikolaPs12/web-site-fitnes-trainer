from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import LoginForm
from app.extensions import db
from app.models.users import User

from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вы успешно вошли в систему.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Неверный email или пароль. Попробуйте еще раз.', 'danger')
    return render_template('user/login.html', form=form)