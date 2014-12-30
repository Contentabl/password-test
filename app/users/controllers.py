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

users = Blueprint('users', __name__)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@users.route('/testing/', methods=['GET'])
def testing():
    return "HEYHEY"


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
		login_user(new_user)

		return redirect("/users/dashboard/")


@users.route('/login', methods=['POST'])
def login():
	"""
	A function to log a user in
	ARGS:
		email, password
	"""
	# Redirect if they are already logged in
	if current_user.is_authenticated():
		return redirect('/users/dashboard/')

	email = request.json["email"]
	password = request.json["password"]

	user = User.query.filter_by(email=email).first()
	if not user:
		return jsonify({
			'status' : 0,
			'message' : 'We did not find an account with that email'
			})
	#if user.chec_p



@users.route('/dashboard/', methods=['POST', 'GET'])
def dashboard():
	return render_template('dashboard/profile_page.html')

