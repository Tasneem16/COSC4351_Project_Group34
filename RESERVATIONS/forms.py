from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import TextAreaField, TelField, StringField, PasswordField, SubmitField, BooleanField, IntegerField, \
    DateField, TimeField, SelectMultipleField
from datetime import datetime, time
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tableres.models import User, Reservation, Tables, Creditcard


# class RegistrationForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')
#
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('That username is taken. Please choose a different one.')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('That email is taken. Please choose a different one.')
# #
class RegistrationForm(FlaskForm):
    fname = StringField('First Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[Length(max=10)])
    mail_add = TextAreaField('Mailing address', validators=[DataRequired()])
    bill_add = TextAreaField('Billing address', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    user_fname = StringField('First name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    user_lname = StringField('Last name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[Length(max=10)])
    mail_add = TextAreaField('Mailing address', validators=[DataRequired()])
    bill_add = TextAreaField('Billing address', validators=[DataRequired()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    # def validate_username(self, username):
    #     if username.data != current_user.username:
    #         user = User.Query.filter_by(username=username.data).first()
    #         if user:
    #             raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class ReservationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    ph_num = TelField('Phone Number')
    num_Guests = IntegerField('Number of Guests', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', description="Select only full hours with 00 in minutes for successful reservation!! i.e.: 11:00", validators=[DataRequired()])
    submit = SubmitField('Submit')

class TableForm(FlaskForm):
    table_slt = SelectMultipleField('Select necessary tables', choices=Tables.query.all())
    submit = SubmitField('submit')

class CreditcardForm(FlaskForm):
    credit_num = IntegerField('Card Number', validators=[DataRequired()])
    name_oncard = StringField('Name on Card', validators=[DataRequired()])
    cvv_num = IntegerField('CVV', validators=[DataRequired()])
    exp_date = DateField('Expiration Date', validators=[DataRequired()])
    billing_add = TextAreaField('Billing Address')
    submit = SubmitField('submit')
