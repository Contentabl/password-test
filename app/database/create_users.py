from app import app, db
from app.users.models import *
from app.users.controllers import *
from app.users.constants import *
import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask import jsonify, session, g
import string, random

# Create sample users for testing purposes
def random_string(length):
	return ''.join(random.choice(string.ascii_letters) for _ in range(length)) 

def decision():
	return random.random() < .5

names = ['Bob', 'Jimmy', 'Aman', 'Vik', 'Jason']
for i in range(5):
	email = names[i] + "@a.com"
	password = "password"
	my_user = User(names[i], email, password)
	my_user.address = random_string(15)
	my_user.phone = random_string(10)
	for day in my_user.week.days:
		day.breakfast = decision()
		day.lunch = decision()
		day.dinner = decision()
		day.snacks = decision()
		day.dessert = decision()
		db.session.add(day)

db.session.commit()
	
