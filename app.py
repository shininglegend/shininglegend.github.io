# This background code written for the Inner Excellence Journaling project
# Written by Titus Murphy. (c) 2023
# The | e filter is for escaping (Built into flask)

from flask import render_template
from datetime import datetime
# We import all the "helper functions" - stored at ./helpers/
from helpers.helpers import *

from helpers.admin_pages import *
from helpers.journal_pages import *
from helpers.user_management import *
from helpers.email_notifs import *

# import the app/db in order to avoid circular imports
from init import app

# May have stolen this function from the finance pset:)
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


# Datetime filter
@app.template_filter()
def format_datetime(value, str="Created"):
    currtime = datetime.now()
    format = "%Y-%m-%d %H:%M:%S" 
    timeCreated = datetime.strptime(value, format)
    diff = currtime - timeCreated
    if diff.days <=1:
        return f"{str} less than a day ago."
    elif diff.days <= 30:
        return f"{str} about {diff.days} day(s) ago."
    else: 
        return f"{str} about {round(diff.days/30)} month(s) ago."


# Handle cool 404 errors 
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=error), 404


# Handle annoying 500 errors
@app.errorhandler(500)
def server_error(error):
    # Send email notifs of problems (Beyond scope of project to be handed in)
    return render_template('error.html', error=error), 500

# Send an email to say the server started
#send_email('jvctext@gmail.com', "[INFO] Server Started", 
#           "Hey, this is just a message to indicated that the server has started.")
#print("Sent init email.")