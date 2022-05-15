from flask import render_template
from . import main
from flask_login import login_required

@main.route('/')
def index():
    '''
    view root function that returns render_template
    '''
    title = 'Welcome to my Blog!'
    
    return render_template('index.html',title = title)

