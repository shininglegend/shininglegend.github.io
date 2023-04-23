# Code written by Titus Murphy for CS-50
""" These functions handle the following pages
- add_client
- client_journals
- (future) clients_list
- respond
"""

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers.helpers import login_required, admin_required
from init import app, db


# Add a client
@app.route("/add-client")
@login_required
@admin_required
def add_client():
    return render_template("add_client.html")

# View Client's journals
@app.route("/client-journals")
@login_required
@admin_required
def client_journals():
    return render_template("client-journals.html")