from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models.task import Task

main = Blueprint('main', __name__)

@main.route('/', methods={'GET', 'POST'})
def home():
	if request.method == 'POST':
		title = request.form['title']
		description = request.form.get('description')
		due_date = request.form.get('due_date')

		task = Task(
			title=title,
			description=description,
			due_date=due_date if due_date else None,
			user_id=1 # Fixed for now
		)
		db.session.add(task)
		db.session.commit()
		return redirect(url_for('main.home'))


	tasks = Task.query.filter_by(user_id=1).order_by(Task.created_at).all()
	return render_template('home.html', tasks=tasks)
