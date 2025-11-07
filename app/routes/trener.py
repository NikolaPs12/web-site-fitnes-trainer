from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from ..models.dbtren import Trener
from ..extensions import db, socketio  
from flask import current_app 
from ..forms import AddTrener
from flask_socketio import emit
from ..functions import save_picture, admin_required

trener_bp = Blueprint('trener', __name__)

@trener_bp.route("/add_trener", methods=["POST", "GET"])
@admin_required
def add_trener():
    form = AddTrener()
    
    if form.validate_on_submit():
        # ✅ Проверяем, был ли загружен файл
        avatar_filename = None
        if form.avatar.data and form.avatar.data.filename:
            avatar_filename = save_picture(form.avatar.data)
        time_slots = []
        start_time = int(form.start_time.data)
        end_time =  int(form.end_time.data)
        for hour in range(start_time, end_time):
            time_slots.append(f"{hour:02d}:00-{hour+1:02d}:00")

        trener = Trener(
            all_name=form.all_name.data,
            avatar=avatar_filename,  # может быть None
            text=form.text.data,
            instagram=form.instagram.data,
            vk=form.vk.data,
            telegram=form.telegram.data,
            whatsapp=form.whatsapp.data,
            list_working_hours=time_slots
        )
        
        try:
            db.session.add(trener)
            db.session.commit()
            flash('Тренер успешно добавлен!', 'success')
            # Очищаем форму после успешного добавления
            return redirect(url_for('trener.add_trener'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении тренера', 'error')
    
    return render_template("trener/add_trener.html", form=form)

@trener_bp.route("/treners", methods=["GET"])
def treners():
    treners = Trener.query.order_by(Trener.id.asc()).all()
    return render_template("trener/all_trener.html", treners=treners)


