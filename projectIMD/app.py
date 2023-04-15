#!/usr/bin/env python3
""" image forgery detection """

import imghdr
import os
from flask import (Flask, render_template,
                   request, flash, redirect,
                   url_for, escape, session,
                   flash, Response, abort)
import pymysql as mysqldb
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

Img = __import__('models').Img
# from models import Img
db = __import__('db').db
init_db = __import__('db').init_db
# from db import init_db, db

USER='postgres'
PASSWORD='wel1234come'
HOST='localhost'
PORT='5432'
DB='IMD'

extensions_list = ['.jpg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.jpeg', '.jpe', '.jfif', '.jif', 'jfi', '.heif', '.ind', '.svg', '.ai', '.eps']

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5120 * 5120
app.config['UPLOAD_EXTENSIONS'] = extensions_list
app.config['UPLOAD_PATH'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///images.db'
# app.config['SQLALCHEMY_DATABASE_URI']= "mysql+mysqldb://root:password@localhost/IMD"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://${USER}:${PASSWORD}@${HOST}/{DB}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'bulabla'

init_db(app)

def image_validator(stream):
    """
    Validates an image file stream by checking the file header
    and determining the format of the file.
    Args:
        stream (file stream): A file stream object containing an image file.
    Returns:
        A string with the format extension (e.g., '.png', '.jpg', etc.)
        if the format is recognized, or `None` if the format is not recognized.
    Raises:
        None.
    """
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/home', strict_slashes=False)
def index():
    """
    home page
    """
    return render_template('index.html')


@app.route('/about', strict_slashes=False)
def abt():
    """
    about page
    """
    return render_template('about.html')


@app.route('/login', strict_slashes=False)
def log():
    """
    login page
    """
    return render_template('login.html')


@app.route('/signup', strict_slashes=False)
def sign():
    """
    signup page
    """
    return render_template('signup.html')


@app.route('/_login', methods=['POST', 'GET'], strict_slashes=False)
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
        if e_mail == request.form['Email'] and passcode == request.form['Password']:
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


@app.route('/upload', methods=['GET', 'POST'], strict_slashes=False)
def upload():
    if request.method=="POST":
        """handles forgery detection"""
        pic = request.files['pic']
        filename = secure_filename(pic.filename)
        # check if the post request has the file part
        if pic not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        # if user does not select file, browser also
        # submit an empty part without filename
        if pic.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if pic != '':
            file_ext = os.path.splitext(pic)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != image_validator(pic.stream):
                abort(400)
            pic.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            # file_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
            pic.save(file_path)
        return '', 204
        if not pic:
            return 'no file uploaded', 404
         
        # mimetype = mimetypes.guess_type(filename)
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        size = os.path.getsize(os.path.join(app.config['UPLOAD_PATH'], filename))
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload', 400

        file_data = pic.read()
        IMG = Img(real_img=file_data,
                  forg_img='',
                  mimetype=mimetype,
                  name=filename,
                  file_path=file_path,
                  size=size)
        return '', 204
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))      
        db.session.add(IMG)
        db.session.commit()
        
        return 'image uploaded succesfully', 200
        
        return redirect((url_for('home')))
    return render_template('index.html',)


@app.route('/get_images/<int:id>', strict_slashes=False)
def get_images(id):
    """return an image of id on request"""
    IMG = Img.query.filter_by(id=id).first()
    
    if not IMG:
        return 'No img found', 404
    
    return Response(IMG.real_img, mimetype=IMG.mimetype)


if __name__ == '__main__':
    """
    :return:
    """
    # db.create_all()
    app.run(debug=True)
