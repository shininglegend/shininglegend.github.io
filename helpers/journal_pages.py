# Code written by Titus Murphy for CS-50
""" These functions handle the following pages
- index (homepage, "/")
- journal (new_entry)
- view_journal
"""

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

from helpers.helpers import *
from init import app, db


# Homepage
@app.route("/")
@login_required
def index():
    return render_template("index.html")

# Journalling page
@app.route("/journal")
@login_required
def journal():
    return render_template("journal.html")

# View Journals page
@app.route("/mjournal")
@login_required
def journal():
    return render_template("journal.html")