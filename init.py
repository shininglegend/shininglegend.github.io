# This background code written for the Inner Excellence Journaling project
# This code is meant to run once to avoid a circular dependancy
# Written by Titus Murphy. (c) 2023


from cs50 import SQL
from flask import Flask
from flask_session import Session
import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Set the log level to DEBUG for this logger
logger.setLevel(logging.DEBUG)

# Create a file handler that logs debug and higher level messages to a file
file_handler = logging.FileHandler('logs.txt')
file_handler.setLevel(logging.DEBUG)

# Create a console handler that logs info and higher level messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# NOTE: This is for development only
#app.config["DEBUG"] = True 
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///journals.db")

# Define if the app is in production or not
production = False