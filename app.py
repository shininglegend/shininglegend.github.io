# This background code written for the Inner Excellence Journaling project
# Written by Titus Murphy. (c) 2023


from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# We import all the "helper functions" - stored at ./helpers/*
from helpers.helpers import *

from helpers.admin_pages import *
from helpers.journal_pages import *
from helpers.user_management import *

# import the app/db in order to avoid circular imports
from init import app, db


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response






# Response page
@app.route("/response")
@login_required
@admin_required
def response():
    request.args.get("userid")
    return render_template("response.html")





# Contact-us page
@app.route("/contact-us")
def contact_us():
    return render_template("contact-us.html")
