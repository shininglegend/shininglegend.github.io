from cs50 import SQL
from flask import redirect, session, render_template
from functools import wraps

from init import app, db

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
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check the user id
        user_status = db.execute("SELECT admin FROM users WHERE id=?", session.get("user_id"))[0]["admin"]
        if user_status == False:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# If you done messed up! (This is temporary)
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

# This code checks whether a code is an admin code and whether it is valid
def check(code, email):
    # TODO: Implement this properly!
    return True, True