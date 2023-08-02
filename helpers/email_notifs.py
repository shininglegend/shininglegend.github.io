# This file handles sending notification emails.

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from init import logger

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

