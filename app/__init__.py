from flask import Flask, g, session, redirect, url_for, render_template
import os
import datetime
from flask.ext.sqlalchemy import SQLAlchemy
# Import Flask-Admin
from flask.ext.admin import Admin

# Import the flask login handler
from flask.ext.login import LoginManager, current_user
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configurations
# normal configuration anyway
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# create the flask login handler
lm  = LoginManager()
lm.init_app(app)
lm.login_view = "TODO" "users.login"

admin = Admin(app, name="MealsToHeal")

assets = Environment(app)

from app.users.controllers import users

# Registering blueprints
app.register_blueprint(users, url_prefix='/users')

from app.users.models import *
@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
	print "hey"
	return render_template('index/index.html')