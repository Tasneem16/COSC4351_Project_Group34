from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/loginscreen', methods=['GET', 'POST'])        #Logging in
def login():
    if request.method == 'POST':        #Tells webserver to take data entered in the form
        email = request.form.get('email')
        password = request.form.get('password1')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.reserve'))       #if password and email matched one in database, it takes them to the screen to reserve
            else:
                flash('Incorrect password, try again.', category='error')       #notifies of wrong password
        else:
            flash('Email does not exist.', category='error')        #notifies account with that email doesnt exist

    return render_template("loginscreen.html", user=current_user)


@auth.route('/logout')      #Logging out
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')       #notifies user they have signed out
    return redirect(url_for('auth.login'))


@auth.route('/registerpage', methods=['GET', 'POST'])       #creating an account
def sign_up():
    if request.method == 'POST':        #Tells webserver to take data entered in the form
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        phone_no = request.form.get('phone')
        mail_add = request.form.get('mail_address')
        prefer_payment = request.form.get('prefered_payment')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')        #checks if account exists already
        elif len(first_name) < 2 or len(first_name) > 20:
            flash('First name must be greater than 2 and less than 20 characters.', category='error')       #validating all credentials entered
        elif len(last_name) < 2 or len(last_name) > 20:
            flash('Last name must be greater than 2 and less than 20 characters.', category='error')
        elif len(phone_no) != 10:
            flash('Phone number should be a 10-digit number.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_user = User(user_fname=first_name, user_lname=last_name, email=email, phone=phone_no, mailing_add=mail_add,
                           prefered_payment=prefer_payment, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)        #pushing to database
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("registerpage.html", user=current_user)
