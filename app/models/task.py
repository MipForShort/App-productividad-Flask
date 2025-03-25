from app import db
from datetime import datetime

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	description = db.Column(db.Text, nullable=True)
	is_done = db.Column(db.Boolean, default=False)
	due_date = db.Column(db.DateTime, nullable=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
