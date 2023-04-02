#!/usr/bin/env python3
""" image forgery detection """

from flask import (Flask, render_template,
                   request, flash, redirect,
                   url_for, escape, session,
                   flash)

app = Flask(__name__)
app.secret_key = 'bulabla'


@app.route('/', strict_slashes=False)
def index():
    """
    home page
    """
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'], strict_slashes=False)
def login():
    """" handles user login"""
    if request.method == 'POST':
        e_mail = request.form['Email']
        passcode = request.form['Password']
        if email == e_mail and password == passcode:
            flash('login successful', 'success')
            return redirect(url_for('index'))
        else:
            return render_template('signup.html')
        
    if request.method == 'GET':
        e_mail = request.args.get('Email')
        passcode = request.args.get('Password')
        if e_mail = request.form['Email'] and passcode == request.form['Password']:
            return redirect(url_for('index'))      
    
    # return render_template('login.html', name=name, email=email, password=password)


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
