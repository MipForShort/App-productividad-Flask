from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.rout('/')
def home():
	return render_template('home.html')
