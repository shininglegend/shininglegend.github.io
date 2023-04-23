# Code written by Titus Murphy for CS-50
""" These functions handle the following pages
s = singular entry, m = multiple entries
- index (homepage, "/") (m)
- journal (new_entry) (s)
- view_journal (s)
"""

from flask import Flask, redirect, render_template, request, session, url_for

from helpers.helpers import *
from init import app, db


# TODO: Homepage
@app.route("/")
@login_required
def index():
    return render_template("index.html")

# TODO: Journalling page
@app.route("/journal")
@login_required
def journal():
    # I'll use url_for()
    return render_template("journal.html")

# TODO: Review an individual Journal's page
@app.route("/journals/<int:post_id>")
@login_required
def journals(post_id):
    return render_template("journal.html")