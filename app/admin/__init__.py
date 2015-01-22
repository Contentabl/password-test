from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
from werkzeug import check_password_hash, generate_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import login_required, login_user, current_user
from app import db, lm, app, admin
from app.users.models import *
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView

class MyView(BaseView):
	@expose('/')
	def index(self):
		print("ACCESSING")
		if (app.config['DEBUG']) or (current_user.is_authenticated() and current_user.email in app.config['ADMINS']):
			return self.render('index.html')
		else:	
			abort(401)

	def is_accessible(self):
		return True
		#! this should obviously be changed before production. In fact a lot of this should be changed


class DataAdmin(ModelView):
	def __init__(self, model, session, **kwargs):
		super(DataAdmin, self).__init__(model, session, **kwargs)

	def is_accessible(self):
		return 'chef' in session


admin.add_view(DataAdmin(User, db.session))
admin.add_view(DataAdmin(Week, db.session))
admin.add_view(DataAdmin(Day, db.session))
admin.add_view(DataAdmin(Diet, db.session))