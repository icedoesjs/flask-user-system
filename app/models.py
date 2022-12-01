from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.String(50), nullable=False)

    def __init__(self, first_name, last_name, username, email, password, date):
        self.firstname = first_name
        self.lastname = last_name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.date_created = date

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    