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

@users.route('/testing/', methods=['GET'])
def testing():
    return "HEYHEY"