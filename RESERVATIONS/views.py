from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, logout_user
from .models import User, Profile, Quote
from datetime import datetime
from datetime import date
from . import db

quote_info = []
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('views.homepage'))
    
@views.route('/profilepage', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        if len(full_name) < 2 or len(full_name) > 50:
            flash('Full name must be greater than 2 and less than 50 characters.', category='error')
        elif len(address1) < 2 or len(address1) > 100:
            flash('Address must be greater than 2 and less than 100 characters.', category='error')
        elif len(city) < 2 or len(city) > 100:
            flash('City must be greater than 2 and less than 100 characters.', category='error')
        elif len(state) != 2:
            flash('Reselect state.', category='error')
        elif len(zipcode) < 5 or len(zipcode) > 9:
            flash('Zipcode must be greater than 5 and no more than 9 characters.', category='error')
        else:
            print("current_user id is :", current_user.id)
            new_user_profile = Profile(full_name=full_name, address1=address1, address2=address2, city=city,
                                       state=state, zipcode=zipcode, user_id=current_user.id)
            db.session.add(new_user_profile)
            db.session.commit()

            flash('Profile created/updated!', category='success')
            return redirect(url_for('views.fuel_quote_form'))

    user = User.query.get(current_user.id)
    profile_list = user.user_profile
    if profile_list:
        if len(profile_list) > 1:
            del (profile_list[:-1])
        cur_profile_id = profile_list[0].id
        user_profile = Profile.query.get(cur_profile_id)
        user_address1 = user_profile.address1
        user_address2 = user_profile.address2
        user_city = user_profile.city
        user_state = user_profile.state
        user_zipcode = user_profile.zipcode
        user_fullname = user_profile.full_name

        return render_template("profilepage.html", user=current_user, full_name=user_fullname, address1=user_address1,
                           address2=user_address2, city=user_city, state=user_state, zipcode=user_zipcode)
    else:
        return render_template("profilepage.html", user=current_user)

@views.route('/fuel-quote', methods=['GET', 'POST'])
def fuel_quote_form():
    user = User.query.get(current_user.id)
    profile_list = user.user_profile
    if profile_list:
        if len(profile_list) > 1:
            del(profile_list[:-1])
        cur_profile_id = profile_list[0].id
        user_profile = Profile.query.get(cur_profile_id)
        if user_profile.address2 == '':
            user_address = user_profile.address1 + ', ' + user_profile.city
        else:
            user_address = user_profile.address1 + ', ' + user_profile.address2 + ', ' + user_profile.city
        user_state = user_profile.state
        user_zipcode = user_profile.zipcode
        print("the user's address is: ", user_address)
        print("the user's state is: ", user_state)
        print("the user's zipcode is: ", user_zipcode)

        if request.method == 'POST':
            request_gallons = request.form.get('Total_Gallons_Requested')
            request_date = request.form.get('delivery_date')
            request_address = request.form.get('delivery_Address')
            today_date = date.today()
            if float(request_gallons) < 0:
                flash('Gallons Requested cannot be negative. Please enter a valid number!', category='error')
            elif float(request_gallons) == 0:
                flash('Gallons Requested cannot be zero. Please enter a valid number!', category='error')
            elif datetime.strptime(request_date, '%Y-%m-%d').date() < today_date:
                flash('Delivery Date cannot be a past date. Please enter a valid date!', category='error')
            else:
                quote_history = Quote.query.get(current_user.id)
                if quote_history:
                    history_flag = 1
                else:
                    history_flag = 0
                quote_result = get_price(user_state, history_flag, float(request_gallons))
                print("suggest price is: ", quote_result[0], "total price is: ", quote_result[1])
                global quote_info
                quote_info = [request_gallons, request_address, request_date, quote_result[0], quote_result[1]]
                flash('Suggest price created!', category='success')
                return redirect(url_for('views.fuel_quote_result'))
        return render_template("quote.html", user=current_user, address=user_address, state=user_state, zipcode=user_zipcode)
    else:
        flash('Please create a user profile with a valid address before filling the Quote Form!', category='error')
        return render_template("quote.html", user=current_user)

@views.route('/fuel-quote-result', methods=['GET', 'POST'])
def fuel_quote_result():
    global quote_info
    print('quote_result ', quote_info)
    if request.method == 'POST':
        
        new_quote_result = Quote(gallons_requested=quote_info[0],
                                 delivery_address=quote_info[1],
                                 date=quote_info[2],
                                 suggest_price=quote_info[3],
                                 total_price=quote_info[4], user_id=current_user.id
                                 )
        db.session.add(new_quote_result)
        db.session.commit()

        flash('Quote result added!', category='success')
        return redirect(url_for('views.fuel_quote_history'))

    return render_template("quote_result.html", user=current_user, gallons_requested=quote_info[0],
                           delivery_address=quote_info[1], delivery_date=quote_info[2], suggest_price=quote_info[3],
                           total_price=quote_info[4])


@views.route('/fuel-quote-history', methods=['GET', 'POST'])
def fuel_quote_history():
    user = User.query.get(current_user.id)
    history_list = user.user_quote
    return render_template("quotehistory.html", user=current_user, history_list=history_list)


@views.route('/viewprofile', methods=['GET', 'POST'])
def viewprofile():
    user = User.query.get(current_user.id)
    profile_list = user.user_profile
    if profile_list:
        if len(profile_list) > 1:
            del (profile_list[:-1])
        cur_profile_id = profile_list[0].id
        user_profile = Profile.query.get(cur_profile_id)
        if user_profile.address2 == '':
            user_address = user_profile.address1
        else:
            user_address = user_profile.address1 + ', ' + user_profile.address2

        user_city = user_profile.city
        user_state = user_profile.state
        user_zipcode = user_profile.zipcode
        user_fullname = user_profile.full_name
        user_idname = user.first_name

        return render_template("viewprofile.html", user=current_user, user_name=user_idname, full_name=user_fullname, address=user_address,
                           city=user_city, state=user_state, zipcode=user_zipcode)
    else:
        return render_template("viewprofile.html", user=current_user)

@views.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template("homepage.html", user=current_user)

@views.route('/Assignments', methods=['GET', 'POST'])
def Assignments():
    return render_template("Assignments.html", user=current_user)

@views.route('/Aboutus', methods=['GET', 'POST'])
def Aboutus():
    return render_template("AboutUs.html", user=current_user)

@views.route('/home_login_page')
def home_login():
    logout_user()
    return redirect(url_for('auth.login'))

@views.route('/home_registration')
def home_registration():
    logout_user()
    return redirect(url_for('auth.sign_up'))

##########################################################################################
def get_price(state, request_frequent, request_gallons):   
    current_price = 1.5
    profit_factor = 0.1

    if state == 'TX':
        location_factor = 0.02
    else:
        location_factor = 0.04

    if request_frequent >= 1:
        history_factor = 0.01
    else:
        history_factor = 0

    if request_gallons > 1000:
        gallon_factor = 0.02
    else:
        gallon_factor = 0.03

    

    margin = current_price * (location_factor - history_factor + gallon_factor + profit_factor)
    suggested_price = current_price + margin
    total_due = suggested_price * request_gallons

    results = [round(suggested_price, 2), round(total_due, 2)]
    
    return results
