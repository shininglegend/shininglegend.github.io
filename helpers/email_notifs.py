# This file handles sending notification emails.

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import render_template, request
from helpers.helpers import *
from init import logger, app, db

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
if not SENDGRID_API_KEY:
    logger.critical("Sendgrid API key not found.")
    raise Exception("Sendgrid Api Key not found.")
SENDER_EMAIL = 'titus@innerexcellence.com'

def send_email(to_email, type, body):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject=type,
        html_content=body)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.debug(response.status_code)
        logger.debug(response.body)
        logger.debug(response.headers)
    except Exception as e:
        logger.error(str(e))

# TODO: Email preferences page
@app.route("/email-preferences", methods=["GET", "POST"])
def email_preferences():
    if request.method == "GET":
        # Get their current preferences
        # Check if they're in the database
        user = db.execute("SELECT * FROM email_preferences WHERE user_id=?", session['user_id'])
        if not user:
            # Add them to the database, including their email
            email = db.execute("SELECT email FROM users WHERE id=?", session['user_id'])
            db.execute("INSERT INTO email_preferences (user_id, email) VALUES (?, ?)", session['user_id'], email[0]['email'])
            return render_template("email-preferences.html", preferences)
        else:
            # Get their current preferences
            preferences = db.execute("SELECT * FROM email_preferences WHERE user_id=?", session['user_id'])
            return render_template("email-preferences.html", preferences=preferences)
    else:
        # Check which ones are selected
        pass
