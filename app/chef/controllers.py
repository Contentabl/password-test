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


