from flask import Blueprint, render_template, flash, redirect, url_for, g
from .db import get_db

bp = Blueprint('maintence', __name__, url_prefix='/maintence')

@bp.route('car-history/<id>', methods=('GET',))
def maintence_history(id):
    db = get_db()
    
    # Check if the user is logged in
    if g.user is None:
        flash("You need to log in to view maintenance history.")
        return redirect(url_for('home'))

    # Query the database to check if the user is authorized to view maintenance history
    if g.user_type == 'mechanic':
        # Check if the mechanic has an appointment with the car
        appointment = db.execute(
            'SELECT * FROM appointments WHERE mechanic_id = ? AND car_registration = ?',
            (g.user['mechanic_id'], id)
        ).fetchone()
        if appointment is None:
            flash("You don't have permission to view this car's maintenance history.")
            return redirect(url_for('home'))

    elif g.user_type == 'customer':
        # Check if the car belongs to the customer
        car = db.execute(
            'SELECT * FROM cars WHERE car_id = ? AND owner_email = ?',
            (id, g.user['email'])
        ).fetchone()
        if car is None:
            flash("You don't have permission to view this car's maintenance history.")
            return redirect(url_for('home'))

    else:
        flash("You don't have permission to view this car's maintenance history.")
        return redirect(url_for('home'))

    # Retrieve car details
    car = db.execute(
        'SELECT * FROM cars WHERE car_id = ?', (id,)
    ).fetchone()

    # Retrieve all appointments for the car
    appointments = db.execute(
        'SELECT * FROM appointments WHERE car_id = ?', (id,)
    ).fetchall()

    return render_template("car_maintenance_page.html", car=car, appointments=appointments)
