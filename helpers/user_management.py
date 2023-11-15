# Code written by Titus Murphy for CS-50
""" These functions handle the following pages
- login
- logout
- (future) manage_account
- register
"""
from datetime import date, datetime, timedelta
from flask import flash, redirect, render_template, request, session, url_for, get_flashed_messages
from werkzeug.security import check_password_hash, generate_password_hash

from helpers.helpers import apology, login_required
from helpers.email_notifs import send_email
from helpers.admin_pages import gencode
from init import app, db


# Dictionary to store email cooldowns
cooldowns = {}
cooldown_duration = 300 # 5 minutes
reset_duration = 1800  # 30 minutes


# Login page (stolen from my finance pset but like it was so well written :) 
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Preserve flashed messages
    flashed_messages = session.get('_flashes', [])

    # Clear the session
    session.clear()

    # Restore flashed messages
    session['_flashes'] = flashed_messages

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide email.", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide a valid password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password.")
            return render_template("login.html")

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
    

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    # Get user details
    user = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])[0]
    
    # If POST, update account details
    if request.method == "POST":
        # Update name if provided
        if request.form.get("name"):
            db.execute("UPDATE users SET name = ? WHERE id = ?", request.form.get("name"), session["user_id"])
        
        # Update password if provided
        if request.form.get("password"):
            # Check if passwords match
            if request.form.get("password") != request.form.get("confirmation"):
                return render_template("account.html", error="Those passwords do not match.", email=user['email'], name=user['name'])
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("password")), session["user_id"])
        flash("Your account details have been updated (if you changed anything).")
        return redirect("/")
    return render_template("account.html", email=user['email'], name=user['name'])

    
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


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        #print("Received POST request on forgot-password.")
        email = request.form['email']

        # Check cooldown for requesting reset links
        last_request_time = cooldowns.get(email, {}).get('last_request_time', None)
        if last_request_time:
            if datetime.now() - last_request_time < timedelta(seconds=cooldown_duration):
                flash("You need to wait before requesting another password reset.")
                return redirect(url_for('forgot_password'))
        
        # Check cooldown for sending reset links
        last_send_time = cooldowns.get(email, {}).get('last_send_time', None)
        if last_send_time:
            if datetime.now() - last_send_time < timedelta(seconds=reset_duration):
                flash("A reset link has already been sent. Please check your email.")
                return redirect(url_for('login'))

        # Check if their email exists in the database, if not, only pretend something happened
        user = db.execute("SELECT * FROM users WHERE email=?", email)
        if not user:
            flash("If your email is in our database, a reset link has been sent to your email.")
            return redirect(url_for('login'))
        # Send reset password link
        print("User exists.")
        reset_code = gencode(email, False, "reset")
        print(reset_code)
        body = f'''
            <h3>Hello! Someone requested a password reset for {email}.</h3><hr>
            If it was you, click <a href="{url_for('reset_password', token=reset_code, _external=True)}">here</a> to reset your password.<br>
            Or copy and paste the following link into your browser:<br>
            {url_for('reset_password', token=reset_code, _external=True)}<br>
            <strong>Please note that all previous links have been invalidated.</strong>
        '''
        # Make a custom timestamp per hour to ensure a new thread is created
        send_email(email, f"Password Reset for IX Journals", body)

        # Update cooldowns
        cooldowns[email] = {
            'last_request_time': datetime.now(),
            'last_send_time': datetime.now()
        }

        flash("If your email is in our database, a reset link has been sent to your email.")
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

# Set up the actual reset page
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        # Check if the token is in the database and valid
        # Check their code and email
        validity = check(token, request.form.get("email"))[1]
        passcode = request.form.get("new_password")
        email = request.form.get("email")
        print(validity, passcode)
        if (not validity) or (not passcode) or (not email):
            flash("That code was invalid, or you didn't provide an email / password.")
            return redirect("/forgot-password")
        elif validity != True:
            flash(f"That code has expired as of {validity}. Try again.")
            return redirect("/forgot-password")
        
        # Check to ensure their passwords match
        if passcode != request.form.get("confirm_password"):
            flash("Those passwords do not match.")
            return redirect(url_for("reset-password", token=token))

        # Update password if provided
        elif passcode:
            db.execute("UPDATE users SET hash = ? WHERE email = ?", generate_password_hash(passcode), email)
            # Ensure there are no other valid codes to prevent reuse
            db.execute("UPDATE codes SET valid = NULL WHERE email = ?", email)
            flash("Your password has been updated.")
            return redirect("/login")
        else:
            flash("You didn't provide a new password, or they didn't match. Please try again.")
            return render_template("reset-password.html", token=token)
    return render_template("reset-password.html", token=token)