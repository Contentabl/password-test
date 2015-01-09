from app import db
from flask import jsonify, g
import uuid, datetime, json
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
from app.users.constants import *

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	email = db.Column(db.String(120), unique=True)
	pw_hash = db.Column(db.String(200))
	salt = db.Column(db.String(40))
	address = db.Column(db.Text)
	phone = db.Column(db.String(20))
	dietary_restrictions = db.Column(db.String(150))

	week = db.relationship("Week", backref = db.backref('user'), uselist=False)
	days = db.relationship("Day", backref = db.backref('user'))

	def __init__(self, name=None, email=None, password=None):
		self.name = name
		self.email = email
		# randomly generate new salt, then hash the password
		self.salt = str(uuid.uuid4().get_hex())
		self.time_of_signup = datetime.datetime.now()
		self.set_password(password)
		my_week = Week(self)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password + self.salt)

	def is_active(self):
	    return True

	def is_authenticated(self):
		return True

	def is_anonymous(self):
	    return False

	def get_id(self):
	    return unicode(self.id)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password + self.salt)

	def __repr__(self):
		return '<User %r>' % (self.name)

	def getMetaData(self):
		try:
			restrictions = json.loads(self.dietary_restrictions)
		except:
			restrictions = []
		my_dict = {}
		for restriction in dietary_restrictions_list:
			my_dict[restriction] = (restriction in restrictions)

		return {
			'id' : self.id,
			'name' : self.name,
			'email' : self.email,
			'address' : self.address,
			'phone' : self.phone,
			'dietary_restrictions' : my_dict
		}

class Week(db.Model):
	"""
	The Week object with refs to all days of the week
	"""
	__tablename__ = 'week'
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	notes = db.Column(db.Text, default = "")
	days = db.relationship("Day", backref = db.backref('week'))

	def __init__(self, user=None):
		self.user = user
		for i in range(7):
			my_day = Day(i, self, user)

	def __repr__(self):
		return '<Week for %r>' % (self.user.name)

class Day(db.Model):
	"""
	Contains the users orders for a particular day of the week
	"""
	__tablename__ = "day"
	id = db.Column(db.Integer, primary_key = True)
	week_id = db.Column(db.Integer, db.ForeignKey('week.id'))
	day_of_week = db.Column(db.Integer)

	breakfast = db.Column(db.Boolean, default = False)
	lunch = db.Column(db.Boolean, default = False)
	dinner = db.Column(db.Boolean, default = False)
	snacks = db.Column(db.Boolean, default = False)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, day_of_week=None, week=None, user=None):
		self.week = week
		self.day_of_week = day_of_week
		self.user = user

	def __repr__(self):
		return 'Day {0} for {1}'.format(days_array[self.day_of_week], self.week.user.name)



