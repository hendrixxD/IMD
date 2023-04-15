#!/usr/bin/env python3
"""db class"""
db = __import__('db').db

class Img(db.Model):
    """db class for images"""
    id = db.Column(db.Integer, primary_key=True)
    real_img = db.Column(db.Text, unique=True, nullable=False)
    forg_img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.String(255), nullable=True)


def __init__(self, img, name, mimetype):
    self.real_img = real_img
    self.forg_img = forg_img
    self.name = name
    self.mimetype = mimetype
