from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.task import Task
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/', methods={'GET', 'POST'})
def home():
	if request.method == 'POST':
		title = request.form['title']
		description = request.form.get('description')

		due_date_str = request.form.get('due_date')
		due_date = None
		if due_date_str:
			due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')

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

@main.route('/toggle_done/<int:task_id>', methods=['POST'])
def toggle_done(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for('main.home'))

@main.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.home'))
