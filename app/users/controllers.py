from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify, make_response, json
from werkzeug import check_password_hash, generate_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle
from flask.ext.login import login_required, login_user, current_user, logout_user
from datetime import datetime, timedelta
import base64, random, string, math
import requests

from app import db, lm, app, assets
from app.users.models import *
from app.users.emails import *

users = Blueprint('users', __name__)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@users.route('/signup/', methods=['POST'])
def signup():
	"""
	The function to sign a new user up
	ARGS:
		name, email, password
	"""
	name = request.json['name']
	email = request.json['email']
	password = request.json['password']

	# Check that all the information is passed correctly
	if not name or not email or not password:
		return jsonify({
			'status' : 0,
			'message' : "We need you to fill out all the information."
		})

	# Make sure they are not already logged in
	#if 'auth' in session or current_user.is_authenticated():
	#	return redirect("TODO")

		# Make sure that email is available
	check_user = User.query.filter_by(email=request.json['email']).first()
	if check_user:
		return jsonify({
			'status': 0,
			'message': 'That email has already been registered'
		})

	# Create a new user and add them to the database
	else:
		new_user = User(name, email, password)
		db.session.add(new_user)
		db.session.commit()
		session['auth'] = True
		session['user_id'] = new_user.id
		login_user(new_user)

		return jsonify({
			'status' : 1
			})


@users.route('/login/', methods=['POST'])
def login():
	"""
	A function to log a user in
	ARGS:
		email, password
	"""
	# Redirect if they are already logged in
	if current_user.is_authenticated():
		return jsonify({
			'status' : 1
			})

	email = request.json["email"]
	password = request.json["password"]

	user = User.query.filter_by(email=email).first()
	if not user:
		return jsonify({
			'status' : 0,
			'message' : 'We did not find an account with that email'
			})
	# Check their password
	if user.check_password(password):
		login_user(user)
		session['auth'] = True
		session['user_id'] = user.id
		return jsonify({
			'status' : 1
			})
	# If the password is not correct
	else:
		return jsonify({
			"status" : 0,
			"message" : "That password is incorrect. Please contact us if you need to reset it."
			})

@users.route('/auth/', methods=['GET'])
def auth():
	if current_user:
		return redirect('users/dashboard/')
	return render_template('login/login.html')


@users.route('/dashboard/', methods=['POST', 'GET'])
@login_required
def dashboard():
	return render_template('dashboard/profile_page.html')

@users.route('/chef/', methods=['POST', 'GET'])
def chef():
	return render_template('dashboard/chef.html')


@users.route('/logout/', methods=['POST', 'GET'])
@login_required
def logout():
    """ This function logs out a user """
    logout_user()
    session.pop('auth', None)
    session.pop('user_id', None)
    return redirect('/')

@users.route('/info/', methods=['GET'])
@login_required
def info():
	""" Returns a Users info as a JSON string
	ARGS: None
	RET: Look at the users model to see all the fields
	"""
	return jsonify({
		'info': current_user.getMetaData()
		})

@users.route('/profile/update/', methods = ['POST'])
@login_required
def update():
	"""
	Updates a users info
	Dietary Restrictions should be a list of strings. 
	"""
	user = current_user
	if 'name' in request.json:
		user.name = request.json['name']
	if 'email' in request.json:
		existing_user = User.query.filter_by(email = request.json['email']).first()
		if not existing_user:
			user.email = request.json['email']
	if 'address' in request.json:
		user.address = request.json['address']
	if 'phone' in request.json:
		user.phone = request.json['phone']

	db.session.add(user)
	db.session.commit()

	return jsonify({
		'status' : 1,
		'message' : "Your profile was successfully updated"
		})

@users.route('/diet/update/', methods = ['POST'])
@login_required
def update_diet():
	"""
	Used as an endpoint for updating a users diet
	ARGS: 'diet', a list of strings of dietary restrictions
	"""

	diet_object = Diet(current_user)
	diet_object.dietary_restrictions = json.dumps(request.json['diet'])
	current_user.dietary_restrictions = json.dumps(request.json['diet'])
	db.session.add(diet_object)
	db.session.add(current_user)
	db.session.commit()
	return jsonify({
		'status' : 1
		})

@users.route('/order/', methods = ['POST'])
@login_required
def order():
	order = request.json['order']
	for day in days_array_list:
		day_object = Day.query.filter_by(user = current_user, day_of_week = days_array_reverse[day]).first()
		current_order = order[day]
		day_object.breakfast = current_order[0]
		day_object.lunch = current_order[1]
		day_object.dinner = current_order[2]
		day_object.snacks = current_order[3]
		day_object.dessert = current_order[4]
		db.session.add(day_object)
		db.session.commit()

	return jsonify({
		'status' : 1
		})

@users.route('/chefpage/', methods = ['GET'])
def chefpage():
	"""
	Returns a list of all the meals for the week 
	ARGS: None
	RET: A very complicated JSON object
	"""
	ret = {}
	for i in range(7):
		day_ret = {'Breakfast':[], 'Lunch':[], 'Dinner':[], 'Snacks':[], 'Dessert':[]}
		day_objects = Day.query.filter_by(day_of_week = i).all()
		for day_object in day_objects:
			if day_object.breakfast:
				day_ret['Breakfast'].append({'user' : day_object.week.user.getMetaData(), 'notes' : day_object.week.notes})
			if day_object.lunch:
				day_ret['Lunch'].append({'user' : day_object.week.user.getMetaData(), 'notes' : day_object.week.notes})
			if day_object.dinner:
				day_ret['Dinner'].append({'user' : day_object.week.user.getMetaData(), 'notes' : day_object.week.notes})
			if day_object.snacks:
				day_ret['Snacks'].append({'user' : day_object.week.user.getMetaData(), 'notes' : day_object.week.notes})
			if day_object.dessert:
				day_ret['Dessert'].append({'user' : day_object.wee.user.getMetaData(), 'notes' : day_object.week.notes})
		day_name = days_array[i]
		ret[day_name] = day_ret

	return jsonify({'data': ret})

@users.route('/chefview/', methods= ['GET'])
def chefview():
	"""
	Renders the chef view
	"""
	return render_template('dashboard/chef.html')

@users.route('/dietview/', methods = ['GET'])
def dietview():
	"""
	Returns the history of people's diets
	"""
	ret = []
	users = User.query.all()
	for user in users:
		user_dict = user.getMetaData()
		history = []
		diets = Diet.query.filter_by(user=user).all()
		for diet in diets:
			date = diet.date.strftime("%m %d %Y")
			print diet.dietary_restrictions
			if not diet.dietary_restrictions:
				diet = []
			else:
				diet = json.loads(diet.dietary_restrictions)
			history.append({'date' : date, 'diet' : diet})
		user_dict['history'] = history
		ret.append(user_dict)

	return jsonify({'data': ret})

@users.route('/sendemail/', methods = ['GET'])
def sendemail():
	send_all_emails()
	return redirect('/')



