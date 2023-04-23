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
@app.route("/journal", methods=["GET", "POST"])
@login_required
def journal():
    if request.method == "POST":
        # Save the entry
        pass
    # Make a new journal 
    else:
        #journal_id = db.execute("INSERT INTO journals (user_id) VALUES (?)", session.get("user_id"))
        return redirect(url_for('journals', post_id = 1))

# TODO: Review an individual Journal's page
@app.route("/journals/<int:post_id>", methods=["GET", "POST"])
@login_required
def journals(post_id):
    # If this is a new request
    return render_template("journal.html", post_id=post_id)
    # Otherwise, save the entry.