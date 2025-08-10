from flask import Flask, render_template, request, redirect, url_for, Blueprint
from .extensions import db, login_manager, migrate
from .config import Config
from .routes.main import main
from .routes.zapis import zapis
from .routes.contact import contact_bp
from .routes.prise import prise_bp

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(zapis)
    app.register_blueprint(contact_bp)
    app.register_blueprint(prise_bp)
    db.init_app(app)
    migrate.init_app(app, db)


    with app.app_context():
        db.drop_all()  # Удаляем все таблицы перед созданием
        db.create_all()    
    return app