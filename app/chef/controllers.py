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
from app.chef.decorators import *
from app.users.freshbooks import *
from app.users.constants import *
from app.users.constants import *
from config import MAIL_PASSWORD

chef = Blueprint('chef', __name__)


@chef.route('/dashboard/', methods = ["GET"])
@chef_required
def render_dashboard():
	return render_template("dashboard/chef_dashboard.html")

@chef.route('/delete_user/', methods = ["POST"])
@chef_required
def delete_user():
	email = request.form['email']
	user = User.query.filter_by(email = email).first()

	if not user:
		return "No user with that email"

	else:
		name = user.name
		for day in user.week.days:
			db.session.delete(day)
		db.session.delete(user.week)
		status = delete_freshbookuser(user.freshbooks_id)
		db.session.delete(user)
		db.session.commit()
		if status == "ok":
			return "Successfully deleted " + name
		else:
			return "Deleted " + name + " but couldn't delete from freshbooks"

@chef.route('/reset_password/', methods = ["POST"])
@chef_required
def reset_password():
	email = request.form['email']
	password = request.form['password']

	user = User.query.filter_by(email = email).first()

	if not user:
		return "No user with that email"

	else:
		user.set_password(password)
		db.session.add(user)
		db.session.commit()
		return "Password successfully updated"

@chef.route('/freshbooks/invoices/', methods = ["POST"])
@chef_required
def update_freshbooks():
	"""
	Generates invoices for all the users
	ARGS: None
	"""
	ret = ""
	users = User.query.all()
	meals = {}
	for user in users:
		meals['breakfasts'] = 0
		meals['lunches'] = 0
		meals['dinners'] = 0
		meals['snacks'] = 0
		meals['desserts'] = 0 
		for day in user.week.days:
			if day.breakfast:
				meals['breakfasts'] += 1
			if day.lunch:
				meals['lunches'] += 1
			if day.dinner:
				meals['dinners'] += 1
			if day.snacks:
				meals['snacks'] += 1
			if day.dessert:
				meals['desserts'] += 1

		resp = create_invoice(meals, user.freshbooks_id)
		if resp == "ok":
			ret += "Created invoice for " + user.name +"<br>"
		else:
			ret += "Error creating invoice for " + user.name + "<br>"
	return ret

@chef.route('/freshbooks/single_invoice/', methods = ["POST"])
@chef_required
def create_single_invoice():
	"""
	Generates invoice for a specific user
	ARGS: email
	"""
	email = request.form['email']
	user = User.query.filter_by(email=email).first()
	if not user:
		return "No user with email " + email
	else:
		meals = {}
		meals['breakfasts'] = 0
		meals['lunches'] = 0
		meals['dinners'] = 0
		meals['snacks'] = 0
		meals['desserts'] = 0 
		for day in user.week.days:
			if day.breakfast:
				meals['breakfasts'] += 1
			if day.lunch:
				meals['lunches'] += 1
			if day.dinner:
				meals['dinners'] += 1
			if day.snacks:
				meals['snacks'] += 1
			if day.dessert:
				meals['desserts'] += 1

		resp = create_invoice(meals, user.freshbooks_id)
		if resp == "ok":
			return "Created invoice for " + user.name +"<br>"
		else:
			return "Error creating invoice for " + user.name + "<br>"		

@chef.route('/edit/', methods = ['POST'])
@chef_required
def edit_meals():
	"""
	Accessed from /users/chefUser/ when the chef changes meals in the grid
	ARGS:
		email: the users email
		data: a dict with different days of the week
	"""
	email = request.json['email']
	user = User.query.filter_by(email=email).first()
	if not user:
		return jsonify({
			'status' : 0,
			'message' : "Error retrieving user"
			})
	data = request.json['data']

	for day in days_array_list:
		if day in data:
			day_object = Day.query.filter_by(user=user, day_of_week = days_array_reverse[day]).first()
			for meal in data[day]:
				if meal == 1:
					day_object.breakfast = not day_object.breakfast
				if meal == 2:
					day_object.lunch = not day_object.lunch
				if meal == 3:
					day_object.dinner = not day_object.dinner
				if meal == 4:
					day_object.snacks = not day_object.snacks
				if meal == 5:
					day_object.dessert = not day_object.dessert
			db.session.add(day_object)
	db.session.commit()
	return jsonify({
		'status' : 1
		})



