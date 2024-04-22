from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager 

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='helloworld'
    #get the database store from sqlite
    app.config['SQLALCHEMY_DATABASE_URI']= f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth 

    

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
     
    #import the models file
    from .models import User
    #createdb 
    create_database(app)

    #set loginmanager
    login_manager= LoginManager()
    login_manager.login_view="auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app 

#create the database if it does not exits
def create_database(app):
    if not path.exists("AutoBookrr/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("created database!")