import os
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import sha256_crypt
import gc
from functools import wraps
import indicoio
from sentiment import evaluate_emotions

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/images')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/idlab'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column('id', db.Integer, primary_key=True)
    fname = db.Column('fname', db.Unicode)
    lname = db.Column('lname', db.Unicode)
    photo_id = db.Column('photo_id', db.Unicode)
    permission = db.Column('permission', db.Unicode)
    last_access = db.Column('last_access', db.DateTime)
    card_id = db.Column('card_id', db.Integer)
    
    
    def __init__(self, fname, lname, photo_id, permission, last_access, card_id):
        self.fname = fname
        self.lname = lname
        self.photo_id = photo_id
        self.permission = permission
        self.last_access = last_access
        self.card_id = card_id
        
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

import id.views