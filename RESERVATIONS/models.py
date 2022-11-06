from datetime import datetime
from tableres import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.png')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.id}', '{self.email}', '{self.image_file}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_fname = db.Column(db.String(20), nullable=False)
    user_lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.Integer)
    mailing_add = db.Column(db.String(100), nullable=False)
    billing_add = db.Column(db.String(100), nullable=False)
    earned_pts = db.Column(db.Integer, default=0)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    reservations = db.relationship('Reservation', backref='customer', lazy=True)
    creditcards = db.relationship('Creditcard', backref='customer', lazy=True)

    def __repr__(self):
        return f"User('{self.user_fname}', '{self.user_lname}', '{self.id}', '{self.email}', '{self.image_file}')"




# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"

#
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     user_fname = db.Column(db.String(20), nullable=False)
#     user_lname = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     phone = db.Column(db.Integer)
#     mailing_add = db.Column(db.String(100), nullable=False)
#     billing_add = db.Column(db.String(100), nullable=False)
#     earned_pts = db.Column(db.Integer, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.png')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='user', lazy=True)
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.id}', '{self.email}', '{self.image_file}')"


class Reservation(db.Model):
    res_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer)
    no_guest = db.Column(db.Integer, nullable=False)
    res_date = db.Column(db.Date, nullable=False)
    res_time = db.Column(db.Time, nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.table_id'))
    creditcards = db.relationship('Creditcard', backref='reservation', lazy=True)
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
    exp_date = db.Column(db.Date, nullable=False)
    billing_add = db.Column(db.String(200))


    def __repr__(self):
        return f"Creditcard('{self.credit_num}', '{self.cvv_num}', '{self.exp_date}','{self.name_oncard}', '{self.billing_add}')"


class Tables(db.Model):
     table_id = db.Column(db.Integer, primary_key=True)
     capacity = db.Column(db.Integer, nullable=False)
     reservations = db.relationship('Reservation', backref='table', lazy=True)

     def __repr__(self):
        return f"Tables('{self.table_id}', '{self.capacity}', '{self.reservations}')"



