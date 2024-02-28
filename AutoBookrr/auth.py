from flask import Blueprint,render_template,redirect,url_for,request,flash
from . import db
from . models import User
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash


auth = Blueprint("auth", __name__)


#this will render the html pages 
@auth.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        email = request.form.get("email")
        password = request.form.get("password")

        #check if the user 
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("logged in!",category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password not right',category='error')
        else:
            flash('Email does not exist',category='error')


    return render_template("login.html")

@auth.route("/register",methods=['GET','POST'])
def register():
    if request.method =='POST':
        email= request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #check if the email exists and if it does not exists
        email_exists=User.query.filter_by(email=email).first()
        user_exists = User.query.filter_by(username= username).first()
        #logic for register
        if email_exists:
            flash('the email already exists',category='error')
        elif user_exists:
            flash('the username exists',category='error')
        elif password1 != password2:
            flash('password does not match', category='error')
        #check the length of the username and password
        elif len(username) <2:
            flash('Username too short ',category ='error')
        elif len(password1)<6:
            flash('password is too short',category='error')
        elif len(email)<4:
            flash('email invalid ',category ='error')
        else:
            new_user=User(email=email,username=username, password=generate_password_hash(password1,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            #login user after created 
            login_user(new_user,remember=True)

            flash('User created')
            return redirect(url_for('views.home'))


    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    #logout the user
    logout_user()
    return redirect(url_for("views.home"))