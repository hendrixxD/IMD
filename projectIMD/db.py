#!/usr/bin/env python3
"""initialize the database environment"""

from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

db = SQLAlchemy()

# function to initialize the database and create tables
def init_db(app):
    db.init_app(app)
    # Migrate(app, db)
    # create the logs tables if db doesn't exist
    with app.app_context():
        db.create_all()