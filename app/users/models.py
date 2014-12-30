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



	def __init__(self, name=None, email=None, password=None):
		self.name = name
		self.email = email
		# randomly generate new salt, then hash the password
		self.salt = str(uuid.uuid4().get_hex())
		self.time_of_signup = datetime.datetime.now()
		self.set_password(password)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password + self.salt)

	def is_active(self):
	    return True

	def is_anonymous(self):
	    return False

	def get_id(self):
	    return unicode(self.id)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password + self.salt)

	def __repr__(self):
		return '<User %r>' % (self.name)