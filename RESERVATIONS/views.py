from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, logout_user, login_required
from .models import User, Reservation, Creditcard, Tables
from datetime import datetime
import pytz
from . import db

guest_res = []
views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for('views.reserve'))
    else:
        return redirect(url_for('views.home'))

@views.route("/homescreen", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_no = request.form.get('phone')
        guests = request.form.get('guests')
        res_date = request.form.get('res_date')
        res_time = request.form.get('res_time')
        time_zone = pytz.timezone('America/Chicago')
        time_now = datetime.now(time_zone)
        current_time = time_now.strftime("%H:%M")

        user = User.query.filter_by(email=email).first()

        availseats = Reservation.query.filter_by(res_date=res_date, res_time=res_time)
        total = int(guests)

        for x in availseats:
            total += x.no_guest

        if user:
            flash('Email already exists. Please log in to reserve.', category='error')
        elif len(name) < 2 or len(name) > 50:
            flash('Name must be greater than 2 and less than 50 characters.', category='error')
        elif len(phone_no) != 10:
            flash('Phone number should be a 10-digit number.', category='error')
        elif float(guests) < 0:
            flash('Number of guests cannot be negative. Please enter a valid number!', category='error')
        elif float(guests) == 0:
            flash('Number of guests cannot be zero. Please enter a valid number!', category='error')
        elif datetime.strptime(res_date, '%Y-%m-%d').date() < time_now.date():
            flash('Reservation Date cannot be a past date. Please enter a valid date!', category='error')
        elif res_time < current_time:
            flash('Reservation Time cannot be a past time. Please enter a valid time!', category='error')
        elif total > 20:
            flash('Seats for the selected date and time are not available. please select other times!!', category='error')
        elif total <= 20:
            new_reservation = Reservation(name=name, email=email, phone=phone_no, no_guest=guests,
                                       res_date=res_date, res_time=res_time)
            db.session.add(new_reservation)
            db.session.commit()
            global guest_res
            guest_res = [name, email, phone_no, guests, res_date, res_time]
            flash('Please create an account for the best user experience!', category='success')
            flash('Please select a table to complete reservation.', category='success')
            return redirect(url_for('views.tables'))

    return render_template('homescreen.html', user=current_user)

@views.route("/aboutpage", methods=['GET', 'POST'])
def about():
    return render_template('aboutpage.html', user=current_user)

@views.route("/selecttable", methods=['GET', 'POST'])
def tables():
    global guest_res
    if request.method == 'POST':
        if current_user.is_authenticated:
            user = User.query.get(current_user.id)
            res_list = user.reservations
            if res_list:
                cur_reserve_id = res_list[-1].res_id
                user_reserve = Reservation.query.get(cur_reserve_id)
                user_res_date = user_reserve.res_date
                user_res_time = user_reserve.res_time
                table = request.form.get('tables')
                booked = Tables.query.filter_by(reserve_date=user_res_date, reserve_time=user_res_time, capacity=table).first()
                if booked:
                    flash('The selected table for the selected date and time is not available. Please select combined tables to reserve.',
                          category='error')
                else:
                    new_table = Tables(capacity=table, reserve_date=user_res_date, reserve_time=user_res_time)
                    db.session.add(new_table)
                    db.session.commit()
                    flash('Your reservation is final and no show will be charged minimum $10.', category='error')
                    flash('Your Table(s) has been reserved.', category='success')
                    user_card = user.creditcards
                    if user_card:
                        if len(user_card) > 1:
                            del (user_card[:-1])
                        return redirect(url_for('views.reserved'))
                    else:
                        return redirect(url_for('views.payments'))

        else:
            resquery = Reservation.query.filter_by(res_date=guest_res[4],
                                                   res_time=guest_res[5])
            for i in resquery:
                table = request.form.get('tables')
                guest_res_date = i.res_date
                guest_res_time = i.res_time
                booked = Tables.query.filter_by(reserve_date=guest_res_date, reserve_time=guest_res_time, capacity=table).first()
                if booked:
                    flash('The selected table for the selected date and time is not available. Please select combined tables to reserve.',
                          category='error')
                    break
                else:
                    new_table = Tables(capacity=table, reserve_date=guest_res_date, reserve_time=guest_res_time)
                    db.session.add(new_table)
                    db.session.commit()
                    flash('Your reservation is final and no show will be charged minimum $10.', category='error')
                    flash('Your Table(s) has been reserved.', category='success')
                    return redirect(url_for('views.guestpayment'))

    return render_template('selecttable.html', user=current_user)

@views.route("/myaccount", methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.get(current_user.id)
    if request.method == 'GET':
        if user:
            user_email = user.email
            user_diner_id = current_user.id
            user_earned_pts = user.earned_pts
            user_firstname = user.user_fname
            user_lastname = user.user_lname
            user_phone = user.phone
            user_mailadd = user.mailing_add
    elif request.method == 'POST':
        if user:
            user.user_fname = request.form.get('firstname')
            user.user_lname = request.form.get('lastname')
            user.phone = request.form.get('phone')
            user.mailing_add = request.form.get('mail_address')
            if len(user.user_fname) < 2 or len(user.user_fname) > 20:
                flash('First name must be greater than 2 and less than 20 characters.', category='error')
            elif len(user.user_lname) < 2 or len(user.user_lname) > 20:
                flash('Last name must be greater than 2 and less than 20 characters.', category='error')
            elif len(user.phone) != 10:
                flash('Phone number should be a 10-digit number.', category='error')
            else:
                db.session.commit()
                flash('Your account has been updated!', category='success')
                return redirect(url_for('views.account'))

    return render_template("myaccount.html", user=current_user, email=user_email, diner_id=user_diner_id,
                           earned_pts=user_earned_pts, first_name=user_firstname, last_name=user_lastname,
                           phone=user_phone, mail_address=user_mailadd)

@views.route("/reserving", methods=['GET', 'POST'])
def reserve():
    user = User.query.get(current_user.id)
    if user:
        user_name = user.user_fname + ' ' + user.user_lname
        user_email = user.email
        user_phone = user.phone

        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone_no = request.form.get('phone')
            guests = request.form.get('guests')
            res_date = request.form.get('res_date')
            res_time = request.form.get('res_time')
            time_zone = pytz.timezone('America/Chicago')
            time_now = datetime.now(time_zone)
            current_time = time_now.strftime("%H:%M")

            availseats = Reservation.query.filter_by(res_date=res_date, res_time=res_time)
            total = int(guests)

            for x in availseats:
                total += x.no_guest

            if float(guests) < 0:
                flash('Number of guests cannot be negative. Please enter a valid number!', category='error')
            elif float(guests) == 0:
                flash('Number of guests cannot be zero. Please enter a valid number!', category='error')
            elif datetime.strptime(res_date, '%Y-%m-%d').date() < time_now.date():
                flash('Reservation Date cannot be a past date. Please enter a valid date!', category='error')
            elif res_time < current_time:
                flash('Reservation Time cannot be a past time. Please enter a valid time!', category='error')
            elif total > 20:
                flash('Seats for the selected date and time are not available. please select other times!!',
                      category='error')
            elif total <= 20:
                new_reservation = Reservation(name=name, email=email, phone=phone_no, no_guest=guests,
                                              res_date=res_date, res_time=res_time, user_id=current_user.id)
                db.session.add(new_reservation)
                db.session.commit()
                flash('Please select a table to complete reservation.', category='success')
                return redirect(url_for('views.tables'))

    return render_template('reserving.html', user=current_user, name=user_name, email=user_email, phone=user_phone)

@views.route("/payments", methods=['GET', 'POST'])
def payments():
    if request.method == 'POST':
        card_no = request.form.get('card_no')
        cvv_code = request.form.get('cvv')
        exp_date = request.form.get('exp_date')
        card_name = request.form.get('card_name')
        bill_add = request.form.get('bill_address')
        time_zone = pytz.timezone('America/Chicago')
        time_now = datetime.now(time_zone)

        if len(cvv_code) != 3:
            flash('Security code should be of 3 digits.', category='error')
        elif datetime.strptime(exp_date, '%Y-%m').date() < time_now.date():
            flash('Expired credit cards are not accepted. Please enter a valid expiry date!', category='error')
        else:
            new_payment = Creditcard(user_id=current_user.id, credit_num=card_no, name_oncard=card_name,
                                     cvv_num=cvv_code, exp_date=exp_date, billing_add=bill_add)
            db.session.add(new_payment)
            db.session.commit()
            flash('Each reservation is final and no show will be charged minimum $10.',category='error')
            flash('Payment information added/updated!', category='success')
            return redirect(url_for('views.reserved'))

    user = User.query.get(current_user.id)
    card_list = user.creditcards
    if card_list:
        if len(card_list) > 1:
            del (card_list[:-1])
        cur_card_id = card_list[0].card_id
        user_card = Creditcard.query.get(cur_card_id)
        user_credit_no = user_card.credit_num
        user_card_name = user_card.name_oncard
        user_cvv = user_card.cvv_num
        user_exp_date = user_card.exp_date
        user_bill_add = user_card.billing_add

        return render_template("payments.html", user=current_user, card_no=user_credit_no, cvv=user_cvv,
                               exp_date=user_exp_date, card_name=user_card_name, bill_address=user_bill_add)
    else:
        return render_template("payments.html", user=current_user)

@views.route("/guestpayment", methods=['GET', 'POST'])
def guestpayment():
    global guest_res
    if request.method == 'POST':
        resquery = Reservation.query.filter_by(name=guest_res[0],
                                      email=guest_res[1],
                                      phone=guest_res[2],
                                      no_guest=guest_res[3],
                                      res_date=guest_res[4],
                                      res_time=guest_res[5])
        for i in resquery:
            card_no = request.form.get('card_no')
            cvv_code = request.form.get('cvv')
            exp_date = request.form.get('exp_date')
            card_name = request.form.get('card_name')
            bill_add = request.form.get('bill_address')
            time_zone = pytz.timezone('America/Chicago')
            time_now = datetime.now(time_zone)

            if len(cvv_code) != 3:
                flash('Security code should be of 3 digits.', category='error')
                break
            elif datetime.strptime(exp_date, '%Y-%m').date() < time_now.date():
                flash('Expired credit cards are not accepted. Please enter a valid expiry date!', category='error')
                break
            else:
                new_payment = Creditcard(res_id=i.res_id, credit_num=card_no, name_oncard=card_name,
                                         cvv_num=cvv_code, exp_date=exp_date, billing_add=bill_add)

                db.session.add(new_payment)
                db.session.commit()
                flash('Your reservation is final and no show will be charged minimum $10.', category='error')
                return redirect(url_for('views.home'))

    return render_template('payments.html', user=current_user)

@views.route("/reservations", methods=['GET', 'POST'])
def reserved():
    user = User.query.get(current_user.id)
    reserve_list = user.reservations
    return render_template("reservations.html", user=current_user, reserve_list=reserve_list)


