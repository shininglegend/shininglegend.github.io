# This background code written for the Inner Excellence Journaling project
# Written by Titus Murphy. (c) 2023

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, admin_required, apology

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///journals.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Homepage 
# <ul class="navbar-nav me-auto mt-2">
#     <li class="nav-item"><a class="nav-link" href="/">Your Journals</a></li>
#     <li class="nav-item"><a class="nav-link" href="/journal">New Entry</a></li>
# </ul>
# <ul class="navbar-nav ms-auto mt-2">
#     <li class="nav-item"><a class="nav-link" href="/logout">Log Out</a></li>
# </ul>
# {% else %}
# <ul class="navbar-nav ms-auto mt-2">
#     <li class="nav-item"><a class="nav-link" href="/register">Register</a></li>
#     <li class="nav-item"><a class="nav-link" href="/login">Log In</a></li>
# </ul>
# {% endif %}
# {% if session["admin"] %}
# <ul>
#     <li class="nav-item"><a class="nav-link" href="/client-journals">Journals</a></li>
#     <li class="nav-item"><a class="nav-link" href="/clients">Clients</a></li>
# </ul>

# View Client's journals
@app.route("/clients-journals")
@login_required
@admin_required
def client_journals():
    pass
# Login page (stolen from my finance pset but like it was so well written :) 
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide a valid password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Journalling page


# Response page


