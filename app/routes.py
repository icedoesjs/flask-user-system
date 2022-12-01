from app import site
from flask import render_template

@site.route('/')
@site.route('/home')
def index():
    return render_template('index.html', config=site.config)

