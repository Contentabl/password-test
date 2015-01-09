import os
from os import environ

DEBUG = os.environ.get('HEROKU') is None
if DEBUG:
	import secret

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'rMUZgdpPkQbLMHuAGWZc'

CSRF_ENABLED = True

JSON_SORT_KEYS = False

if environ.get('SITE_URL') is None:
	SITE_URL = '127.0.0.1:5000'
else:
	SITE_URL = environ.get('SITE_URL')

if 'DATABASE_URL' not in os.environ:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
else:
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'mealstoheal20@gmail.com'
if os.environ.get('MAIL_PASSWORD'):
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
else:
	MAIL_PASSWORD = secret.MAIL_PASSWORD