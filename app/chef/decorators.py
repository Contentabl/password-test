from functools import wraps
from flask import g, request, redirect, url_for, session

def chef_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'chef' not in session:
            return "Please log in as a chef"
        return f(*args, **kwargs)
    return decorated_function