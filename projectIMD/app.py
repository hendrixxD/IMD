#!/usr/bin/env python3
""" image forgery detection """

from flask import (Flask, render_template,
                   request, flash, redirect,
                   url_for)

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """
    :return:
    """
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'], strict_slashes=False)
def login():
    """" handles user login"""
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    try:
        if name == 'admin' and password == 'admin':
            return redirect(url_for('login'))
    except userNotFound:
        return render_template('signup.html')
    
    return render_template('login.html', name=name, email=email, password=password)


@app.route('/register', methods=['POST', 'GET'], strict_slashes=False)
def register():
    """handles user signup
    """
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    return render_template('register.html', name=name, email=email, password=password)


@app.route('/logout', methods=['POST', 'GET'], strict_slashes=False)
def logout():
    """
    handles user sign out
    """
    return render_template('logout.html')



@app.route('/detect_fogery', methods=['POST', 'GET'], strict_slashes=False)
def image():
    """
    handles forgery detection
    """
    return render_template('detect_fogery.html')

    
if __name__ == '__main__':
    """
    :return:
    """
    app.run(debug=True)
