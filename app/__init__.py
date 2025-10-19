from flask import Flask, render_template, request, redirect, url_for, Blueprint
from .extensions import db, login_manager, migrate
from .config import Config
from .routes.main import main
from .routes.booking import zapis
from .routes.contact import contact_bp
from .routes.prise import prise_bp
from .routes.register import register_bp
from .routes.login import login_bp
from .models.users import User


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    app.register_blueprint(register_bp)
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(zapis)
    app.register_blueprint(contact_bp)
    app.register_blueprint(prise_bp)
    app.register_blueprint(login_bp)

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()    
        
    return app