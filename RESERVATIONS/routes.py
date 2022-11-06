import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, Markup
from flask_mail import Message
from tableres import app, db, bcrypt, mail
from tableres.forms import RegistrationForm, LoginForm, ReservationForm, UpdateAccountForm, CreditcardForm, TableForm
from tableres.models import User, Reservation, Tables, Creditcard
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        reservation = Reservation.query.filter_by(user_id=current_user.id)
        return render_template('homelogin.html', reservation=reservation)
    else:
        global formres
        formres = ReservationForm()
        if formres.validate_on_submit():
            reservation = Reservation(name=formres.name.data,
                                      phone=formres.ph_num.data,
                                      email=formres.email.data,
                                      no_guest=formres.num_Guests.data,
                                      res_date=formres.date.data,
                                      res_time=formres.time.data)
            availseats = Reservation.query.filter_by(res_date=formres.date.data, res_time=formres.time.data)
            total = 0
            for x in availseats:
                total += x.no_guest

            if total < 20:
                db.session.add(reservation)
                db.session.commit()
                msg = Message('New Reservation', sender='tempsender6@gmail.com',
                              recipients=['rajbhadola408@gmail.com', formres.email.data])
                bodymsg = 'New reservation made please ensure the seating is available. for more details signin the system.'
                msg.body = bodymsg
                mail.send(msg)
                flash(Markup(
                    'Please <a href="/register" class="alert-link">Create an account</a> for the best user experience!!'),
                      'success')
                return redirect(url_for('paymentout'))

            else:
                flash('Seats for the selected time are not available. please select other times!!', 'error')

        return render_template('reserve.html', title='Reservation', form=formres)


#   return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/tables", methods=['GET', 'POST'])
def tables():
    form2 = TableForm()
    if form2.validate_on_submit():
        reservation = Reservation(Table=form2.table_slt.data)
    return render_template('tables.html', title='tables', form=form2)

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(user_fname=form.fname.data, user_lname=form.lname.data,
                    email=form.email.data, phone=form.phone.data,
                    mailing_add=form.mail_add.data, billing_add=form.bill_add.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.user_fname = form.user_fname.data
        current_user.email = form.email.data
        current_user.user_lname = form.user_lname.data
        current_user.phone = form.phone.data
        current_user.mail_add = form.mail_add.data
        current_user.bill_add = form.bill_add.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.user_fname.data = current_user.user_fname
        form.user_lname.data = current_user.user_lname
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.mail_add.data = current_user.mailing_add
        form.bill_add.data = current_user.billing_add
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
@app.route("/reserve", methods=['GET', 'POST'])

def reserve():
    form1 = ReservationForm()
    if form1.validate_on_submit():
        reservation = Reservation(name=form1.name.data,
                                  email=form1.email.data,
                                  phone=form1.ph_num.data,
                                  no_guest=form1.num_Guests.data,
                                  res_date=form1.date.data,
                                  res_time=form1.time.data,
                                  customer=current_user)
        availseats = Reservation.query.filter_by(res_date=form1.date.data, res_time=form1.time.data)
        total = 0
        for x in availseats:
            total += x.no_guest

        if total < 20:
            db.session.add(reservation)
            db.session.commit()
            msg = Message('New Reservation', sender='tempsender6@gmail.com', recipients=['rajbhadola408@gmail.com', form1.email.data])
            bodymsg = 'New reservation made please ensure the seating is available. for more details signin the system.'
            msg.body = bodymsg
            mail.send(msg)
            resquery = Creditcard.query.filter_by(user_id=current_user.id)
            for i in resquery:
                if current_user.id == i.user_id:
                    return redirect(url_for('payment'))

        else:
            flash('Seats for the selected time are not available', 'failure')
        return redirect(url_for('home'))
    return render_template('reserve.html', title='Reservation', form=form1)




@app.route("/payment", methods=['GET', 'POST'])
def payment():
    paymentform = CreditcardForm()
    if paymentform.validate_on_submit():
        paymentformadd = Creditcard(user_id=current_user.id,
                                    credit_num=paymentform.credit_num.data,
                                    name_oncard=paymentform.name_oncard.data,
                                    cvv_num=paymentform.cvv_num.data,
                                    exp_date=paymentform.exp_date.data,
                                    billing_add=paymentform.billing_add.data)
        db.session.add(paymentformadd)
        db.session.commit()
        flash('Each reservation is final and will be charged appropriate no show charge for missed reservations.','error')
        flash('Your Table has been Reserved!', 'success')
        flash('Payment information added!!', 'success')
        return redirect(url_for('home'))
    return render_template('payment.html', title='payment', form=paymentform)

@app.route("/paymentout", methods=['GET', 'POST'])
def paymentout():
    paymentform = CreditcardForm()
    if paymentform.validate_on_submit():
        resquery = Reservation.query.filter_by(name=formres.name.data,
                                      phone=formres.ph_num.data,
                                      email=formres.email.data,
                                      no_guest=formres.num_Guests.data,
                                      res_date=formres.date.data,
                                      res_time=formres.time.data)
        for i in resquery:
            paymentformadd = Creditcard(res_id=i.res_id,
                                    credit_num=paymentform.credit_num.data,
                                    name_oncard=paymentform.name_oncard.data,
                                    cvv_num=paymentform.cvv_num.data,
                                    exp_date=paymentform.exp_date.data,
                                    billing_add=paymentform.billing_add.data)
        db.session.add(paymentformadd)
        db.session.commit()
        flash('Each reservation is final and will be charged appropriate no show charge for missed reservations.','error')
        flash('Your Table has been Reserved!', 'success')
        flash('Payment information added!!', 'success')
        return redirect(url_for('home'))
    return render_template('payment.html', title='payment', form=paymentform)


# class Reservation(db.Model):
#     res_id = db.column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
#     name = db.Column(db.String, nullable=False)
#     email = db.Column(db.String(120), nullable=False)
#     phone = db.Column(db.Integer)
#     no_guest = db.Column(db.Integer, nullable=False)
#     res_date = db.Column(db.Date, nullable=False)
#     res_time = db.Column(db.Time, nullable=False)
#     table_id = db.Column(db.Integer, db.ForeignKey('table.table_id'))
