from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc2c5762da84768ed6248d780c1869b7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

##ALL THIS IF YOU WANT TO SEND ACCOUNT CREATION EMAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tempsender6@gmail.com'
app.config['MAIL_PASSWORD'] = '@Temp0912'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)
##UNTIL HERE

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from RESERVATIONS import routes

