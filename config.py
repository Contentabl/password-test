import os
from os import environ

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'rMUZgdpPkQbLMHuAGWZc'

CSRF_ENABLED = True

if 'DATABASE_URL' not in os.environ:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
else:
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']