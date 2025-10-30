from flask import Flask, render_template, request, redirect, url_for, Blueprint
from .extensions import db, login_manager, migrate, socketio
from .config import Config
from .routes.main import main
from .routes.booking import zapis
from .routes.contact import contact_bp
from .routes.prise import prise_bp
from .routes.register import register_bp
from .routes.login import login_bp
from .models.users import User
from .routes.chat import chat_bp
from .routes.trener import trener_bp
from .sockets_app.booking_socket import init_socket_booking
from .sockets_app.chat_socket import init_socket_chat

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Сначала инициализируем расширения
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*")  # ✅ Инициализируем здесь

    # Затем регистрируем blueprint'ы
    app.register_blueprint(trener_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(zapis)
    app.register_blueprint(contact_bp)
    app.register_blueprint(prise_bp)
    app.register_blueprint(login_bp)

    init_socket_booking(socketio)
    init_socket_chat(socketio)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()    
        
    return app