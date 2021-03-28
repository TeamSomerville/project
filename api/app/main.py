from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/destination')
def destination():
    return render_template('destination.html')

@main.route('/activity')
def activity():
    return render_template('activity.html')