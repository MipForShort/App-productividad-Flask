from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validar si el usuario ya existe
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('El correo ya está registrado.', 'error')
            return redirect(url_for('auth.register'))

        # Crear un nuevo usuario
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado exitosamente.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Credenciales inválidas. Inténtalo de nuevo.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash('Has iniciado sesión exitosamente.', 'success')
        
        # Redirige a la página que el usuario intentaba antes de ir al login (si existe 'next')
        next_page = request.args.get('next')  # Captura el parámetro 'next' de la URL
        return redirect(next_page or url_for('main.home'))  # Si no hay 'next', redirige a la home
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('auth.login'))
