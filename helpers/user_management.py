# Code written by Titus Murphy for CS-50
""" These functions handle the following pages
- login
- logout
- (future) manage_account
- register
"""

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers.helpers import apology, check
from init import app, db


# Login page (stolen from my finance pset but like it was so well written :) 
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide email", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide a valid password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["admin"] = False if not rows[0]["admin"] else True

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id/adminstatus
    session.clear()
    # Redirect user to login form
    return redirect("/")


# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    # Process adding the user if POST
    if request.method == "POST":
        # Ensure all fields are filled
        if any([not request.form.get("email"), 
               not request.form.get("password"), 
               not request.form.get("confirmation"),
               not request.form.get("regkey")]):
            return render_template("register.html", error="One or more fields were not completed.")

        # Check their code and email
        adminstatus, validity = check(request.form.get("email"), request.form.get("regkey"))
        if not validity:
            return render_template("contact_us.html")
        
        # Add them to the database
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username doesn't already exist and that passwords match
        if len(rows) != 0:
            return render_template("register.html", error="This email already exists in our database.")
        
        # Check to ensure their passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", error="Those passwords do not match.")
        
        # Add the user to the database, hashing their password in the process
        if not request.form.get("name"):
            userid = db.execute("INSERT INTO users (admin, email, hash) VALUES (?, ?, ?)",
                                adminstatus,
                                request.form.get("email"),
                                generate_password_hash(request.form.get("password")))
        # If they actually provided a name
        else:
            userid = db.execute("INSERT INTO users (admin, name, email, hash) VALUES (?, ?, ?, ?)",
                                adminstatus,
                                request.form.get("name"),
                                request.form.get("email"),
                                generate_password_hash(request.form.get("password")))

        # Log them in
        session["user_id"] = userid
        session["admin"] = adminstatus
        return redirect("/")
    else: 
        return render_template("register.html")