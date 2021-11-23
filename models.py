from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from datetime import datetime
 
login = LoginManager()
db = SQLAlchemy()
 
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())
    appointments = db.relationship("Appointment", backref='booking')
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
 
class Appointment(db.Model):
    __tablename__ = "Appointments"

    id = db.Column(db.Integer, primary_key=True) 
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    c_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    service = db.Column(db.String(), nullable=False)
    rooms_persons = db.Column(db.Integer, nullable=True)

@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))