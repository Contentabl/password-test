from app import db
from flask import jsonify, g
import uuid, datetime, json
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	email = db.Column(db.String(120), unique=True)
	pw_hash = db.Column(db.String(200))
	salt = db.Column(db.String(40))