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
    # Make a new journal 
    journal_id = db.execute("INSERT INTO journals (user_id) VALUES (?)", session.get("user_id"))
    # Send them to that journal
    return redirect(url_for('journals', post_id = journal_id))

# Review an individual Journal's page
@app.route("/journals/<int:post_id>", methods=["GET", "POST"])
@login_required
def journals(post_id):
    if request.method == "GET":
        # Check if the post belongs to them
        content = db.execute("SELECT content FROM journals WHERE id=? AND user_id=?", post_id, session["user_id"])
        # If that one doesn't exist, there won't be a match in the database.
        if not content:
            # Send them to a blank slate by redirecting them to /journal
            return redirect('/journal')
        # Otherwise, send them either a prefilled one (if there is one) or the blank one
        content = content[0]['content']
        return render_template("journal.html", post_id = post_id, content = content)
    # Otherwise, save the entry.
    else:
        form_button_name = 'submit_button'

        # Check if there is already one saved with that ID and user
        draft = db.execute("SELECT * FROM journals WHERE id=? AND user_id=?", post_id, session["user_id"])
        # If that one doesn't exist, there won't be a match in the database.
        if not draft:
            # They somehow went to one that they don't own or doesn't exist.
            return redirect('/journal')
        content = request.form['journal']
        
        # Save a draft in the database
        if request.form[form_button_name] == "saveDraft":
            # Save the draft
            db.execute("UPDATE journals SET content=?, submitted=0 WHERE id=? AND user_id=?", content, post_id, session['user_id'])
            return render_template("journal.html", post_id = post_id, content = content, response = "Successfully saved your draft.")
        
        # "Submit" the draft. 
        elif request.form[form_button_name] == "pubAndSend":
            # Submit it to the database
            db.execute("UPDATE journals SET content=?, submitted=1 WHERE id=? AND user_id=?", content, post_id, session['user_id'])
            # TODO: Add automatic email notifications (after the class perhaps)
            return render_template("journal.html", post_id = post_id, content = content, response = "Successfully submitted!")
        
        elif request.form[form_button_name] == "deleteDraft":
            # Delete the draft
            db.execute("DELETE FROM journals WHERE id=? AND user_id=?", post_id, session['user_id'])
            # FIXME: Confirmation? Logs?
            return redirect("/")

        else:
            # If they modified the html or smthg, send them to rickroll as punishment.
            return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")