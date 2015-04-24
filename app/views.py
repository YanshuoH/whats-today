from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('login.html',
                           title='Login')

@app.route('/main')
def main():
    return render_template('main.html',
                           title='Main')

@app.route('/list')
def list():
    return render_template('list.html',
                           title='List')

@app.route('/today')
def today():
    return render_template('today.html',
                           title='Today')

@app.route('/edit')
def edit():
    return render_template('form.html',
                           title='Edit')
