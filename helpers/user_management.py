# Code written by Titus Murphy for CS-50
""" These functions handle the following pages
- login
- logout
- (future) manage_account
- register
"""
from datetime import date, datetime
from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers.helpers import apology
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
        adminstatus, validity = check(request.form.get("regkey"), request.form.get("email"))
        if not validity:
            flash("That code was invalid. Please contact us.")
            return render_template("contact-us.html")
        elif validity != True:
            flash(f"That code has expired as of {validity}. Please contact us for a new one.")
            return render_template("contact-us.html")
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
        userid = db.execute("INSERT INTO users (admin, name, email, hash) VALUES (?, ?, ?, ?)",
                            adminstatus,
                            request.form.get("name") if request.form.get("name") else None,
                            request.form.get("email"),
                            generate_password_hash(request.form.get("password")))

        # Invalidate the code (as by setting date to null)
        remcode(request.form.get("regkey"))

        # Log them in
        session["user_id"] = userid
        session["admin"] = adminstatus
        return redirect("/")
    else: 
        return render_template("register.html")
    
    
# This code checks A: whether a code is an admin code and B: whether it is valid
def check(code, email):
    # Query the database for the code
    code_data = db.execute("SELECT * FROM codes WHERE email=? AND code=?", email.lower(), code.lower())
    # Check if there is a matche, return invalid if not. 
    # We return the same response if fake to avoid them being able to guess a code and an email seperatly, they need to get both right
    if not code_data:
        return False, False
    if not code_data[0]["valid"]:
        return False, False
    # Check if expired
    valid_until = code_data[0]["valid"]
    if datetime.strptime(valid_until, '%Y-%m-%d').date() < date.today():
        return False, valid_until
    
    # Check if it's an admin code
    if code_data[0]["admin"] == 1:
        return True, True
    
    # Otherwise, it's just a normal code.
    return False, True


# Invalidate the code in the database
def remcode(code):
    db.execute("UPDATE codes SET valid=NULL WHERE code=?", code)
