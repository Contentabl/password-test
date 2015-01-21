from flask import Flask, g, session, redirect, url_for, render_template
import os
import datetime
from flask.ext.sqlalchemy import SQLAlchemy
# Import Flask-Admin
from flask.ext.admin import Admin

# Import the flask login handler
from flask.ext.login import LoginManager, current_user
from flask.ext.assets import Environment, Bundle
from config import *

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
lm.login_view = "users.auth"

# For sending emails
from flask.ext.mail import Mail
mail = Mail(app)

# For the Admin Page
admin = Admin(app, name="name")
from app.admin import *

assets = Environment(app)

from app.users.controllers import users
from app.chef.controllers import chef

# Registering blueprints
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(chef, url_prefix='/chef')

from app.users.models import *
@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
	return render_template('index/index.html')

@app.route('/sendemail/', methods = ['GET'])
def emailform():
	return render_template('emails/emailform.html')

from app.users.controllers import sendemail
@app.route('/emailpassword/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    if text == MAIL_PASSWORD:
    	sendemail()
    	return "Email has been sent"
    else:
    	return "Incorrect Password"