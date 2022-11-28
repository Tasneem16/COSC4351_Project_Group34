from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_fname = db.Column(db.String(20), nullable=False)
    user_lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.Integer)
    mailing_add = db.Column(db.String(100), nullable=False)
    earned_pts = db.Column(db.Integer, default=0)
    password = db.Column(db.String(60), nullable=False)
    reservations = db.relationship('Reservation')
    creditcards = db.relationship('Creditcard')

    def __repr__(self):
        return f"User('{self.user_fname}', '{self.user_lname}', '{self.id}', '{self.email}')"

class Reservation(db.Model):
    res_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer)
    no_guest = db.Column(db.Integer, nullable=False)
    res_date = db.Column(db.String(100), nullable=False)
    res_time = db.Column(db.String(100), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.table_id'))
    creditcards = db.relationship('Creditcard')
    def __repr__(self):
        return f"User('{self.user_id}', '{self.res_id}', '{self.res_time}', '{self.res_date}', '{self.no_guest}'," \
               f"'{self.table_id}')"

class Creditcard(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer, db.ForeignKey('reservation.res_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    credit_num = db.Column(db.Integer, nullable=False)
    name_oncard = db.Column(db.String(120), nullable=False)
    cvv_num = db.Column(db.Integer, nullable=False)
    exp_date = db.Column(db.String(100), nullable=False)
    billing_add = db.Column(db.String(200))

    def __repr__(self):
        return f"Creditcard('{self.credit_num}', '{self.cvv_num}', '{self.exp_date}','{self.name_oncard}', '{self.billing_add}')"

class Tables(db.Model):
     table_id = db.Column(db.Integer, primary_key=True)
     capacity = db.Column(db.String(200), nullable=False)
     reserve_date = db.Column(db.String(100), nullable=False)
     reserve_time = db.Column(db.String(100), nullable=False)

     def __repr__(self):
        return f"Tables('{self.table_id}', '{self.capacity}', '{self.reserve_date}', '{self.reserve_time}')"
