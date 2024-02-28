from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


#user database 
class User(db.Model, UserMixin):
    #information for user 
    id = db.Column(db.Integer,primary_key=True)
    email= db.Column(db.String(140), unique=True)
    username=db.Column(db.String(140),unique=True)
    password=db.Column(db.String(140),unique= True)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())

