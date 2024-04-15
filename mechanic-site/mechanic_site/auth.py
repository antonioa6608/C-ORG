from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
import re
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')
'''
validating registration , get email, name, passowrd 
validating mechanic , email, name, ein , zip
'''
def validate_customer_registration_details(email, name, password):
    if not name:
        return 'Username is required.'
    if not email:
        return 'Email is required.'
    elif not password:
        return 'Password is required.'
    elif len(password) < 7:
        return 'Password must be at least 7 characters in length.'
    elif password.upper() == password.lower():
        return "Password must contain at least one upper case and one lowercase letter"
    
    return None

def validate_mechanic_registration_details(email, name, password, ein, zipcode):
    error = validate_customer_registration_details(email, name, password)
    if error != None:
        return error
    if not zipcode:
        return "Zipcode is required"
    if not ein:
        return "EIN is required"
    if not re.fullmatch('\\d{5}(-\\d{4})?$', zipcode):
        return "The zipcode must be a 9 digit zipcode in the format 12345-1234"
    if not re.fullmatch('\\d{2}(-\\d{7})?$', ein):
        return "The EIN must be in the format 12-1234567"
    
    return None


def register_customer_details(data):
    # Check all the items in the form
    for key in ["email", "name", "password"]:
        if key not in dict(data).keys():
            return {"status": "error", "error-message": f"{key[0].upper()}{key[1:]} is required."}


    email = data['email']
    name = data['name']
    password = data['password']
    db = get_db()
    error = validate_customer_registration_details(email, name, password)

    
#no error then update the db customer table 
    if error is None:
        try:
            db.execute(
                "INSERT INTO customers (email, name, hash) VALUES (?, ?, ?)",
                (email, name, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {email} is already registered."
        else:
            return {"status": "succsess"}

    return {"status": "error", "error-message": error}

def register_mechanic_details(data):
    # Check all the items in the form
    for key in ["email", "name", "password", "zipcode", "ein"]:
        if key not in dict(data).keys():
            return {"status": "error", "error-message": f"{key[0].upper()}{key[1:]} is required."}


    email = data['email']
    name = data['name']
    password = data['password']
    zipcode = data['zipcode']
    ein = data['ein']

    print(f"EIN: {ein}")
    db = get_db()
    error = validate_mechanic_registration_details(email, name, password, ein, zipcode)

    if error is None:
        try:
            db.execute(
                "INSERT INTO mechanics (email, name, hash, ein, zipcode) VALUES (?, ?, ?, ?, ?)",
                (email, name, generate_password_hash(password), ein, zipcode),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {email} is already registered."
        else:
            return {"status": "succsess"}

    return {"status": "error", "error-message": error}

def check_login_details_for_table(table):
    def check_login_details(data):
        username = data['email']
        password = data['password']
        db = get_db()
        error = None
        user = db.execute(
            f'SELECT * FROM {table} WHERE email = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['hash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_email'] = user['email']
            session['user_type'] = table[:-1]
            return {"status": "succsess"}

        return {"status": "error", "error-message": error}
    return check_login_details

def check_mechanic_login_details(data):
    pass


def gen_auth_page_func(template, redirect_url, verify_func):
    def wrapper(auth_page_empty_func):
        @functools.wraps(auth_page_empty_func)
        def auth_page():
            if request.method == 'POST':
                response = verify_func(request.form)
                if response["status"] == "succsess":
                    return redirect(url_for(redirect_url))
                flash(response["error-message"])

            return render_template(template)
        return auth_page
    return wrapper


'''
authenicate customer, detail 
'''
@bp.route('/register_customer', methods=('GET', 'POST'))
@gen_auth_page_func("auth/register_customer.html", "auth.customer_login", register_customer_details)
def customer_register():
    pass

@bp.route('/register_mechanic', methods=('GET', 'POST'))
@gen_auth_page_func("auth/register_mechanic.html", "auth.mechanic_login", register_mechanic_details)
def mechanic_register():
    pass

@bp.route('/login-customer', methods=('GET', 'POST'))
@gen_auth_page_func("auth/login_customer.html", "home", check_login_details_for_table("customers"))
def customer_login():
    pass

@bp.route('/login-mechanic', methods=('GET', 'POST'))
@gen_auth_page_func("auth/login_mechanic.html", "home", check_login_details_for_table("mechanics"))
def mechanic_login():
    pass

@bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@bp.before_app_request
def load_logged_in_user():
    user_email = session.get('user_email')
    g.user_type = session.get('user_type')

    if user_email is None:
        g.user = None
    else:
        g.user = get_db().execute(
            f'SELECT * FROM {g.user_type+"s"} WHERE email = ?', (user_email,)
        ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/")

        return view(**kwargs)

    return wrapped_view

def customer_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.customer_login'))
        if g.user_type != "customer":
            return redirect(url_for('auth.mechanic_on_customer_page'))
        

        return view(**kwargs)

    return wrapped_view

def mechanic_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.customer_login'))
        if g.user_type != "customer":
            return redirect(url_for('auth.customer_on_mechanic_page'))
        

        return view(**kwargs)

    return wrapped_view


print("BP: ", bp)
