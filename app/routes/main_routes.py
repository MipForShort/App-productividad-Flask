from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.task import Task
from datetime import datetime
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('index.html')

@main.route('/home', methods=['GET', 'POST'])
@login_required
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
            user_id=current_user.id  # Asocia la tarea al usuario autenticado
        )

        db.session.add(task)
        db.session.commit()
        flash('Tarea agregada exitosamente.', 'success')
        return redirect(url_for('main.home'))

    # Filtra las tareas por el usuario autenticado
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at).all()
    return render_template('home.html', tasks=tasks)

@main.route('/toggle_done/<int:task_id>', methods=['POST'])
@login_required
def toggle_done(task_id):
    task = Task.query.get_or_404(task_id)
    # Asegúrate de que el usuario que está modificando la tarea sea el propietario
    if task.user_id != current_user.id:
        flash('No tienes permiso para modificar esta tarea.', 'error')
        return redirect(url_for('main.home'))

    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for('main.home'))

@main.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    # Asegúrate de que el usuario que está eliminando la tarea sea el propietario
    if task.user_id != current_user.id:
        flash('No tienes permiso para eliminar esta tarea.', 'error')
        return redirect(url_for('main.home'))

    db.session.delete(task)
    db.session.commit()
    flash('Tarea eliminada exitosamente.', 'success')
    return redirect(url_for('main.home'))

