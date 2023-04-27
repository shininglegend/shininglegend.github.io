# Code written by Titus Murphy for CS-50
""" These functions handle the following pages
s = singular entry, m = multiple entries
- add_client (s)
- client_journals (m)
- (future) clients_list (m)
- respond to journal (s)
"""
from flask import Flask, redirect, render_template, request, session

from helpers.helpers import login_required, admin_required, gencode
from init import app, db


# TODO: Add a client
@app.route("/add-client")
@login_required
@admin_required
def add_client():
    return render_template("add_client.html")


# TODO: View Client's journals
@app.route("/client-journals")
@login_required
@admin_required
def client_journals():
    return render_template("client-journals.html")


# TODO: Review an individual Journal's page
@app.route("/respond/<int:post_id>")
@login_required
@admin_required
def respond(post_id):
    return render_template("journals.html")


# TODO: Response page
@app.route("/response")
@login_required
@admin_required
def response():
    request.args.get("userid")
    return render_template("response.html")