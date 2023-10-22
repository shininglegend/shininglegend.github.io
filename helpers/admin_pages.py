# Code written by Titus Murphy for CS-50
""" These functions handle the following pages
s = singular entry, m = multiple entries
- add_client (s)
- client_journals (m)
- (future) clients_list (m)
- respond to journal (s)
"""
from flask import flash, redirect, render_template, request, session, url_for, Blueprint, jsonify
from datetime import date, timedelta
from helpers.helpers import login_required, admin_required
from helpers.email_notifs import send_email
from init import app, db, logger
import secrets, string

# Make an admin blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')

# Add a client (using gencode)
@admin.route("/add-client", methods=["GET", "POST"])
@login_required
@admin_required
def add_client():
    if request.method == "POST":
        email = request.form["newclientemail"].lower()
        if not email:
            flash("Something went wrong. Form Not Filled. Contact support if this keeps happening.")
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
        email_content = f"""<h2>Welcome to Inner Excellence!</h2><hr>
            <h3>We're so glad to have you journalling with us. Your custom registration code is:</h3>
            <h2><u>{code}</u></h2><hr>
            <p>Please visit <a href='{url_for('register', _external=True)}'>ixjournal.com/register</a> to register for your new account.</p><hr>
            <p><i>Hint: You'll need to register using the code above and this email: {email}."""
        send_email(email, "Inner Excellence Journalling Registration", email_content)     
        return redirect(url_for('admin.clients'))
    else:
        return render_template("add_client.html")


# View Client's journals
@admin.route("/client-journals")
@login_required
@admin_required
def client_journals():
    # Needed to specify what I get to avoid having 2 id columns
    journals_new = db.execute("""SELECT journals.id, journals.time_crte, users.name, users.email, journals.content, journals.response FROM journals
                              JOIN users ON journals.user_id = users.id 
                              WHERE journals.submitted=1 AND journals.resp_sent=0 AND journals.content IS NOT NULL
                              ORDER BY journals.time_crte DESC""")
    journals_old = db.execute("""SELECT journals.id, journals.time_crte, users.name, users.email, journals.content, journals.response FROM journals
                              JOIN users ON journals.user_id = users.id 
                              WHERE journals.submitted=1 AND journals.resp_sent=1 AND journals.content IS NOT NULL
                              ORDER BY journals.time_crte DESC""")
    print(journals_new, journals_old)
    return render_template("client-journals.html", journals_new = journals_new, journals_old = journals_old)


# Review an individual Journal's page
@admin.route("/respond/<post_id>", methods=["GET", "POST"])
@login_required
@admin_required
def respond(post_id):
    print("Sending to response.html")
    # Review an individual Journal's page
    if request.method == "GET":
        # Check if the post belongs to them
        journal = db.execute("SELECT content, response FROM journals WHERE id=?", post_id)
        # If that one doesn't exist, there won't be a match in the database.
        if not journal:
            flash("I couldn't locate that journal. Perhaps it was deleted?")
            return redirect('/client-journals')
        # Otherwise, send them either a prefilled one (if there is one) or the blank one
        content = journal[0]['content']
        response = journal[0]['response']
        # TODO: Send some info about the user (Beyond scope of project to be handed in)
        return render_template("response.html", post_id = post_id, content = content, response = response)
    # Otherwise, save the entry.
    else:
        print(request.form)
        form_button_name = 'submit_button'

        # Check if there is one saved with that ID
        draft = db.execute("SELECT * FROM journals WHERE id=?", post_id)
        # If that one doesn't exist, there won't be a match in the database.
        if not draft:
            # They somehow went to one that doesn't exist.
            flash("I couldn't locate that journal. Perhaps it was deleted?")
            return redirect('/client-journals')
        response = request.form['response']
        content = draft[0]["content"]
        
        # Save a draft in the database
        if request.form[form_button_name] == "saveDraftR":
            # Save the draft
            db.execute("UPDATE journals SET response=?, resp_id=?, resp_sent=0 WHERE id=?", response, session['user_id'], post_id)
            flash("I saved your draft response!")
            return render_template("response.html", post_id = post_id, content = content, response = response)
        
        # "Submit" the draft. 
        elif request.form[form_button_name] == "sendResp":
            # Submit it to the database
            db.execute("UPDATE journals SET response=?, resp_id=?, resp_sent=1 WHERE id=?", response, session['user_id'], post_id)
            # TODO: Add automatic email notifications
            flash("I sent your response!")
            return render_template("response.html", post_id = post_id, content = content, response = response)
        
        elif request.form[form_button_name] == "deleteDraftR":
            # Delete the draft
            db.execute("UPDATE journals SET response=Null, resp_id=Null, resp_sent=0 WHERE id=?", post_id)
            flash("I deleted your response.")
            # Log the deletion
            logger.info(f"{session['user_id']} deleted the response for post #{post_id}. It said: \"{response}\"")
            return render_template("response.html", post_id = post_id, content = content)

        else:
            # If they modified the html or smthg, send them to rickroll as punishment.
            return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


# Clients page
@admin.route("/clients")
@login_required
@admin_required
def clients():
    # TODO: Add ability to remove clients (Beyond scope of project to be handed in)
    admins = db.execute("SELECT * FROM users WHERE admin=1 ORDER BY joined")
    clients = db.execute("SELECT * FROM users WHERE admin=0 ORDER BY joined")
    new_clients = db.execute("SELECT * FROM codes WHERE valid IS NOT NULL")
    return render_template("clients.html", admins = admins, clients = clients, new_clients = new_clients)


# Generate and add a new random code
def gencode(email, admin, type="register"):
    print(email, admin, type)
    # Check if one exists already
    old_data = db.execute("SELECT * FROM codes WHERE email=?", email)
    if old_data:
        # Print a message to the log internally and wipe old codes
        print(f"Old code for {email} was wiped. It was {old_data[0]}")
        logger.info(f"Old code for {email} was wiped. It was {old_data[0]}")
        db.execute("DELETE FROM codes WHERE email=?", email)
    # Registration codes: 8 characters, valid for 26 weeks
    if type == "register":
        codelen = 8
        valid_for = timedelta(weeks=26)
        # Generate a code (from https://docs.python.org/3/library/secrets.html)
        while True:
            code = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for i in range(codelen))
            # Make sure it's unique
            if not db.execute("SELECT * FROM codes WHERE code=?", code):
                break

    # Reset codes: url-safe token, valid for 1 hour
    else:
        code = secrets.token_urlsafe().lower()
        valid_for = timedelta(hours=1)
        print(code, " is the code")
    # Add a hashed version to the database, including their email
    validity = date.today() + valid_for
    print(validity)
    db.execute("INSERT INTO codes (email, code, valid, admin) VALUES (?, ?, ?, ?)",
               email, code, validity, 0 if admin != True else 1)
    print(code)
    return code

# Response Autosave
@admin.route("/respond/<int:post_id>/autosave", methods=["POST"])
@login_required
@admin_required
def admin_autosave(post_id):
    draft = db.execute("SELECT * FROM journals WHERE id=?", post_id)
    # If that one doesn't exist, there won't be a match in the database.
    if not draft:
        # They somehow went to one that doesn't exist.
        return redirect(url_for('admin.client_journals'))
    # Get the data sent from the AJAX request
    response = request.form.get('content')
    # Save a draft in the database
    db.execute("UPDATE journals SET response=?, resp_id=? WHERE id=?", response, session['user_id'], post_id)
    print(f"Saved draft {post_id} for {session['user_id']} with content {response}")
    return jsonify(success=True)