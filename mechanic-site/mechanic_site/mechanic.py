from flask import Blueprint, render_template, flash, redirect, url_for, g, request, abort
from .db import get_db

from .auth import validate_mechanic_registration_details

bp = Blueprint('mechanic', __name__, url_prefix='/mechanic')

@bp.route('/edit-profile', methods=['POST', "GET"])
def edit_profile():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        zipcode = request.form.get('zipcode')
        ein = request.form.get('ein')
        
        # Validate form data
        if not name or not zipcode or not ein:
            flash('All fields are required', 'error')
            return redirect(url_for('mechanic.edit_profile'))
        
        error = validate_mechanic_registration_details("email@test.com", name, "FakePass", ein, zipcode)
        if error != None:
            flash(error, 'error')
            return redirect(url_for('mechanic.edit_profile'))

        # Additional validation (e.g., ZIP code format, EIN format)

        # Update profile in the database
        db = get_db()
        db.execute(
            'UPDATE mechanics SET name = ?, zipcode = ?, ein = ? WHERE mechanic_id = ?',
            (name, zipcode, ein, g.user['mechanic_id'])
        )
        db.commit()

        flash('Profile updated successfully', 'success')
        return redirect(url_for('mechanic.profile'))

    db = get_db()
    mechanic = db.execute(
        'SELECT name, zipcode, ein FROM mechanics WHERE mechanic_id = ?',
        (g.user['mechanic_id'],)
    ).fetchone()

    return render_template('mechanic/edit-profile.html', mechanic=mechanic)

@bp.route('/profile')
def profile():
    db = get_db()
    mechanic = db.execute(
        'SELECT name, zipcode, ein FROM mechanics WHERE mechanic_id = ?',
        (g.user['mechanic_id'],)
    ).fetchone()

    if not mechanic:
        abort(404)  # Mechanic not found

    return render_template('mechanic/profile.html', mechanic=mechanic)



def mechanic_dashboard():

    db = get_db()
    # Fetch mechanic's appointments from the database
    appointments = db.execute(
        '''
        SELECT 
            c.name AS customer_name,
            a.start_time AS appointment_time,
            ca.make AS car_make,
            ca.model_number AS car_model,
            a.appointment_status,
            a.appointment_id
        FROM 
            appointments a
        JOIN 
            customers c ON a.customer_email = c.email
        JOIN 
            cars ca ON a.car_id = ca.car_id
        WHERE 
            a.mechanic_id = ?
        ''',
        (g.user['mechanic_id'],)
    ).fetchall()

    return render_template("mechanic/dash.html", appointments=appointments)

@bp.route('/<id>/reviews', methods=('GET',))
def reviews(id):
    db = get_db()

    # Fetch mechanic's name
    mechanic = db.execute(
        'SELECT name, zipcode FROM mechanics WHERE mechanic_id = ?',
        (id,)
    ).fetchone()

    if not mechanic:
        flash("Mechanic not found", "error")
        return redirect("/")  # Or any other appropriate action


    # Fetch reviews for the mechanic
    reviews = db.execute(
        'SELECT c.name AS customer_name, a.review_score, a.review_text, a.start_time '
        'FROM appointments AS a '
        'JOIN customers AS c ON a.customer_email = c.email '
        'WHERE a.mechanic_id = ? AND a.review_score IS NOT NULL',
        (id,)
    ).fetchall()

    print(dict(reviews[0]))

    average_rating = "no reviews"
    
    if len(reviews):
        average_rating = sum([review["review_score"] for review in reviews])/len(reviews)

    return render_template("mechanic/review_page.html",
                           mechanic_name=mechanic['name'],
                           reviews=reviews,
                           average_rating = average_rating,
                           mechanic_zipcode = mechanic['zipcode'])


@bp.route('/confirm_appointment', methods=['POST'])
def confirm_appointment():
    if request.method == 'POST':
        db = get_db()
        # Get the appointment ID from the form data

        appointment_id = request.form.get('appointment_id')
        print("APPP")
        print(request.form)

        # Check if the appointment exists and belongs to the current mechanic
        appointment = db.execute(
            'SELECT * FROM appointments WHERE appointment_id = ? AND mechanic_id = ?',
            (appointment_id, g.user['mechanic_id'])
        ).fetchone()

        if appointment is None:
            # If the appointment doesn't exist or doesn't belong to the mechanic, return an error response
            abort(403)  # Forbidden

        # Update the appointment status to confirmed (assuming status 1 means confirmed)
        db.execute(
            'UPDATE appointments SET appointment_status = 1 WHERE appointment_id = ?',
            (appointment_id,)
        )
        db.commit()

        # Return a success response
        return redirect("/")

    # Handle GET requests to this route
    abort(405)  # Method Not Allowed