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


# View Client's journals
@app.route("/client-journals")
@login_required
@admin_required
def client_journals():
    journals_new = db.execute("SELECT * FROM JOURNALS WHERE submitted=1 AND response IS NULL AND content IS NOT NULL")
    journals_old = db.execute("SELECT * FROM JOURNALS WHERE submitted=1 AND response IS NOT NULL AND content IS NOT NULL")
    return render_template("client-journals.html", journals_new = journals_new, journals_old = journals_old)


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


# Clients page
@app.route("/clients")
@login_required
@admin_required
def clients():
    admins = db.execute("SELECT * FROM users WHERE admin=1 ORDER BY joined")
    clients = db.execute("SELECT * FROM users WHERE admin=0 ORDER BY joined")
    new_clients = db.execute("SELECT * FROM codes")
    return render_template("clients.html", admins = admins, clients = clients, new_clients = new_clients)