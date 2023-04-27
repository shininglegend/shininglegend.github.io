# This background code written for the Inner Excellence Journaling project
# Written by Titus Murphy. (c) 2023


from flask import render_template, request

# We import all the "helper functions" - stored at ./helpers/*
from helpers.helpers import *

from helpers.admin_pages import *
from helpers.journal_pages import *
from helpers.user_management import *

# import the app/db in order to avoid circular imports
from init import app


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Contact-us page
@app.route("/contact-us")
def contact_us():
    return render_template("contact-us.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404