from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from . import util
from .auth import customer_required
import re
import functools

bp = Blueprint('customer', __name__, url_prefix='/customer')

@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Update user's profile information in the database
        db = get_db()
        db.execute(
            'UPDATE customers SET name = ?, email = ? WHERE email = ?',
            (name, email, email)
        )
        db.commit()

        flash('Profile updated successfully', 'success')
        return redirect(url_for('customer.profile'))

    db = get_db()
    customer = db.execute(
        'SELECT name, email FROM customers WHERE email = ?',
        (g.user['email'],)
    ).fetchone()

    return render_template('customer/edit-profile.html', customer=customer)

# Additional route to display the user's profile after editing
@bp.route('/profile')
def profile():
    # Fetch the user's profile information from the database
    db = get_db()
    user = db.execute(
        'SELECT name, email FROM customers WHERE email = ?',
        (g.user['email'],)
    ).fetchone()

    return render_template('customer/profile.html', user=user)

def validate_form(form):
    # Check if a suitable time range has been selected on the calendar
    start_time = form.get('start_time')
    end_time = form.get('end_time')

    if not start_time or not end_time:
        return False

    # Check if new car option is selected and new car fields are empty
    car_select = form.get('car')
    if car_select == 'new_car':
        make = form.get('make')
        model_number = form.get('model_number')
        registration_number = form.get('registration_number')

        if not make or not model_number or not registration_number:
            return False

    # Check if description of the problem is empty
    description = form.get('description')
    if not description.strip():
        return False

    return True

def process_booking(form, mechanic_id):
    db = get_db()
    # Extract form data
    car_registration = form.get('car')
    start_time = form.get('start_time').replace("T", " ").replace("Z", "000")
    end_time = form.get('end_time').replace("T", " ").replace("Z", "000")
    description = form.get('description')

    # Handle new car addition if applicable
    if car_registration == 'new_car':
        make = form.get('make')
        model_number = form.get('model_number')
        registration_number = form.get('registration_number')

        db.execute(
            'INSERT INTO cars (make, model_number, registration, owner_email, image_url) VALUES (?, ?, ?, ?, ?)',
            (make, model_number, registration_number, g.user['email'], util.get_car_image(model_number, registration_number))
        )
        db.commit()
        # Get the newly added car's registration number
        car_registration = registration_number

    # Find the car ID based on the registration number
    car_id = db.execute('SELECT car_id FROM cars WHERE registration = ?', (car_registration,)).fetchone()['car_id']

    # Insert the appointment into the database
    db.execute(
        '''
        INSERT INTO appointments 
        (customer_email, mechanic_id, car_id, start_time, end_time, appointment_description, appointment_status) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (g.user['email'], mechanic_id, car_id, start_time, end_time, description, 0)
    )
    db.commit()

    # Retrieve the ID of the newly created appointment
    appointment_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

    return appointment_id

@bp.route('booking_form/<id>', methods=('GET','POST'))
def booking_form(id):
    
    db = get_db()
    if request.method == 'POST':
        # Handle form submission
        if validate_form(request.form):
            process_booking(request.form, id)
            flash('Appointment booked successfully', 'success')
            return redirect(url_for('customer.booking_success', appointment_id=id))
        else:
            flash('Failed to book appointment. Please check your input.', 'error')

    mechanic = db.execute(
        '''
        SELECT mechanics.*, AVG(appointments.review_score) AS average_rating
        FROM mechanics
        LEFT JOIN appointments ON mechanics.mechanic_id = appointments.mechanic_id
        WHERE mechanics.mechanic_id = ?
        GROUP BY mechanics.mechanic_id
        ''',
        (id,)
    ).fetchone()

    # Fetch customer's cars
    customer_cars = db.execute(
        'SELECT * FROM cars WHERE owner_email = ?',
        (g.user['email'],)
    ).fetchall()

    # Fetch existing appointments for the mechanic
    appointments = db.execute(
        '''
        SELECT 
            start_time, 
            end_time 
        FROM 
            appointments 
        WHERE 
            mechanic_id = ? 
        ''',
        (id,)
    ).fetchall()

    return render_template("customer/create_appointment.html", mechanic=mechanic, customer_cars=customer_cars, appointments=appointments)

@bp.route('/booking_success/<appointment_id>', methods=('GET',))
@customer_required
def booking_success(appointment_id):
    db = get_db()
    appointment = db.execute(
        '''
        SELECT 
            mechanics.name AS mechanic_name, 
            mechanics.zipcode AS mechanic_zipcode, 
            cars.make AS car_make,
            cars.model_number AS car_model_number,
            appointments.start_time AS start_time,
            appointments.end_time AS end_time,
            appointments.appointment_description AS description
        FROM 
            appointments
        JOIN
            mechanics ON appointments.mechanic_id = mechanics.mechanic_id
        JOIN
            cars ON appointments.car_id = cars.car_id
        WHERE 
            appointments.appointment_id = ?
        ''',
        (appointment_id,)
    ).fetchone()

    print(appointment)

    return render_template("customer/booking-succsess.html", appointment=appointment)

@bp.route('/find_mechanics', methods=('GET',))
def find_mechanics():
    db = get_db()
    mechanics = db.execute('''
        SELECT
            m.mechanic_id, 
            m.name, 
            AVG(a.review_score) AS avg_rating, 
            m.zipcode 
        FROM 
            mechanics m 
        LEFT JOIN 
            appointments a ON m.mechanic_id = a.mechanic_id 
        GROUP BY 
            m.name, m.zipcode
    ''').fetchall()
    return render_template("customer/find_mechanics.html", nearby_mechanics=mechanics)

@bp.route('/your-cars', methods=('GET', 'POST'))
@customer_required
def your_cars():
    if request.method == 'POST':
        make = request.form['make']
        model_number = request.form['model_number']
        registration_number = request.form['registration_number']

        db = get_db()
        db.execute(
            'INSERT INTO cars (make, model_number, registration, owner_email, image_url) VALUES (?, ?, ?, ?, ?)',
            (make, model_number, registration_number, g.user['email'], util.get_car_image(model_number, registration_number))
        )
        db.commit()

        flash('New car added successfully', 'success')
        return redirect(url_for('customer.your_cars'))

    db = get_db()
    customer_email = g.user['email']

    # Fetch the customer's cars from the database
    customer_cars = db.execute(
        'SELECT * FROM cars WHERE owner_email = ?',
        (customer_email,)
    ).fetchall()


    return render_template("customer/cars.html", customer_cars=customer_cars)

@bp.route('/appointments', methods=('GET', 'POST'))
@customer_required
def appointments():
    return render_template("customer/appointments.html")