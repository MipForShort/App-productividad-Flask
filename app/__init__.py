from flask import Flask
from flask_slqalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
	app = Flask(__name__)

	# Config from config.py
	app.config.from_object(app.config.config)

	# Initialize extensions
	db.init_app(app)
	migrate.init_app(app, db)

	# Register blueprint
	from app.routes.main_routes import main
	app.register_blueprint(main)

	return app
