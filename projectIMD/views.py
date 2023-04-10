#!/usr/bin/env python3
""" views"""

from flask import render_template

# handles the home page
def index():
    """
    home page
    """
    return render_template('index.html')


# handles the about page
def abt():
    """
    about page
    """
    return render_template('about.html')


# handles the signup page
def sign():
    """
    signup page
    """
    return render_template('signup.html')

# handls the login page
def log():
    """
    login page
    """
    return render_template('login.html')