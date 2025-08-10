from flask import Flask, render_template, request, redirect, Request, Blueprint, url_for, flash
from ..extensions import db, login_manager, migrate
from ..forms import ZapisForm
from ..models.zapis import Zapis

zapis = Blueprint('zapis', __name__)

@zapis.route('/appoint', methods=['GET', 'POST'])
def zap():
    form = ZapisForm()
    if form.validate_on_submit():
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        zapis = Zapis(name=name, last_name=last_name, email=email)
        try:
            db.session.add(zapis)
            db.session.commit()
            flash('Appointment successfully created!', 'success')               
        except Exception as e:
            print(str(e))    
            flash('Error creating appointment. Please try again.', 'danger')
    return render_template('zap/zapis.html', form=form)