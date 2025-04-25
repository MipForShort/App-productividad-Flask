from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Config from config.py
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from app.routes.main_routes import main
    from app.routes.auth_routes import auth  # <-- IMPORTA EL BLUEPRINT
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')  # <-- REGISTRO DEL BLUEPRINT

    # Import User model after app is initialized to avoid circular import
    from app.models.user import User

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User  # Retrasa la importación
    return User.query.get(int(user_id))

