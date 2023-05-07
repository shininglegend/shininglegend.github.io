# Code written by Titus Murphy for CS-50
""" These functions handle the following pages
s = singular entry, m = multiple entries
- add_client (s)
- client_journals (m)
- (future) clients_list (m)
- respond to journal (s)
"""
from flask import Flask, flash, redirect, render_template, request, session
from datetime import date, timedelta
from helpers.helpers import login_required, admin_required
from init import app, db
import secrets, string

# Add a client (using gencode)
@app.route("/add-client", methods=["GET", "POST"])
@login_required
@admin_required
def add_client():
    if request.method == "POST":
        email = request.form["newclientemail"].lower()
        if not email:
            flash("Something went wrong. Please contact IT support. FormNotFilled")
            return redirect("/")
        # Admin
        print(request.form.getlist("admincheck"))
        if request.form.getlist("admincheck"):
            code = gencode(email, True)
            flash(f'{email} was successfully added as admin. Code: {code}')
        else:
            code = gencode(email, False)
            flash(f'{email} was successfully added. Code: {code}')
        # Redirect the user to the clients list so they can find the code     
        return redirect("/clients")
    else:
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
@app.route("/respond/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_required
def respond(post_id):
    # Review an individual Journal's page
    if request.method == "GET":
        # Check if the post belongs to them
        content = db.execute("SELECT content FROM journals WHERE id=?", post_id)
        # If that one doesn't exist, there won't be a match in the database.
        if not content:
            flash("I couldn't locate that journal. Perhaps it was deleted?")
            return redirect('/client-journals')
        # Otherwise, send them either a prefilled one (if there is one) or the blank one
        content = content[0]['content']
        # TODO: Send some info about the user (Beyond scope of project to be handed in)
        return render_template("response.html", post_id = post_id, content = content)
    # Otherwise, save the entry.
    else:
        pass


# Clients page
@app.route("/clients")
@login_required
@admin_required
def clients():
    # TODO: Add ability to remove clients
    admins = db.execute("SELECT * FROM users WHERE admin=1 ORDER BY joined")
    clients = db.execute("SELECT * FROM users WHERE admin=0 ORDER BY joined")
    new_clients = db.execute("SELECT * FROM codes WHERE valid IS NOT NULL")
    return render_template("clients.html", admins = admins, clients = clients, new_clients = new_clients)


# Generate and add a new random code
def gencode(email, admin):
    # Check if one exists already
    old_data = db.execute("SELECT * FROM codes WHERE email=?", email)
    if old_data:
        # Check if it is invalid (versus expired)
        if not old_data[0]["valid"]:
            return 
    # Generate a code (from https://docs.python.org/3/library/secrets.html)
    while True:
        code = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for i in range(8))
        # Make sure it's unique
        if not db.execute("SELECT * FROM codes WHERE code=?", code):
            break
    # Add a hashed version to the database, including their email
    validity = date.today() + timedelta(weeks=26)
    print(validity)
    db.execute("INSERT INTO codes (email, code, valid, admin) VALUES (?, ?, ?, ?)",
               email, code, validity, 0 if admin != True else 1)
    return code