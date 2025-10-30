from flask import abort
from flask_login import current_user
from functools import wraps
import os
import secrets
from PIL import Image
from flask import current_app


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)  # не авторизован
        if not current_user.is_admin:
            abort(403)  # нет прав доступа
        return f(*args, **kwargs)
    return decorated_function


def save_picture(picture_file):
    # ✅ ДОБАВЛЕНО: проверка на None и наличие файла
    if not picture_file or picture_file.filename == '':
        return None
    
    try:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(picture_file.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

        # ✅ Создаем директорию если не существует
        os.makedirs(os.path.dirname(picture_path), exist_ok=True)

        output_size = (600, 400)  # соотношение 3:2
        i = Image.open(picture_file)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn
    except Exception as e:
        print(f"Ошибка при сохранении изображения: {e}")
        return None