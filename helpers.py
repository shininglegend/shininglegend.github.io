from cs50 import db
from flask import redirect, session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///journals.db")

def login_required(f):
    # Decorate routes to require login.
    # The Code for this is borrowed from finance
    # https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    # This checks for admin status
    # Loosely based off the code above
    # Check the user id
    user_status = db.execute("SELECT adminstatus FROM users WHERE id=?", session.get("user_id"))[0]["adminstatus"]

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if user_status == False:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function