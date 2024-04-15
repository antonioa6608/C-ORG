import random
import string

import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

from .db import get_db
from . import util


def generate_fake_email(prefix, num):
    return f'{prefix}{num}@customer.com'


def generate_fake_postcode():
    return f'{random.randint(20001, 20599)}-{random.randint(1000, 9999)}'

def generate_fake_appointments(db, customer_email):
    # Generate a random number of appointments (1 to 3)
    num_appointments = random.randint(1, 3)
    
    car_ids = [car['car_id'] for car in db.execute('SELECT car_id FROM cars WHERE owner_email = ?', (customer_email,)).fetchall()]

    # Current datetime
    current_time = datetime.now()

    for _ in range(num_appointments):
        # Random mechanic ID
        mechanic_id = random.randint(1, 400)

        # Random start time (within the last year for past appointments, within the next week for future appointments)
        if random.choice([True, False]):  # 50% chance for upcoming appointment
            start_time = current_time + timedelta(days=random.randint(1, 7))
        else:
            start_time = current_time - timedelta(days=random.randint(1, 365))

        # Random end time (within 1 to 4 hours from start time)
        end_time = start_time + timedelta(hours=random.randint(1, 4))

        # Random car ID
        car_id = random.choice(car_ids)

        # Insert appointment into database
        db.execute(
            '''
            INSERT INTO appointments 
            (customer_email, mechanic_id, car_id, start_time, end_time, appointment_status) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (customer_email, mechanic_id, car_id, start_time, end_time, 0 if start_time > current_time else 1)  # 0 for upcoming, 1 for past
        )

        # If the appointment is in the past, add a review text and score
        if start_time < current_time:
            review_text = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
            review_score = random.randint(1, 5)

            db.execute(
                '''
                UPDATE appointments 
                SET review_text = ?, review_score = ? 
                WHERE start_time = ? AND customer_email = ? AND mechanic_id = ?
                ''',
                (review_text, review_score, start_time, customer_email, mechanic_id)
            )

    # Commit changes
    db.commit()



@click.command('populate-db')
@with_appcontext
def populate_db_command():
    """Populate the database with example customers, cars, and mechanics."""
    db = get_db()

    # Populate customers
    for i in range(1, 900):
        email = generate_fake_email('test', i)
        password = generate_password_hash('FakePass')
        db.execute(
            'INSERT INTO customers (email, name, hash) VALUES (?, ?, ?)',
            (email, f'Customer {i}', password)
        )
        if i%10 == 0:
            click.echo(f"CUSTOMER: {i}")

        
    # Populate mechanics
    for i in range(1, 401):
        email = generate_fake_email('test', i)
        password = generate_password_hash('FakePass')
        if i <= 100:
            zipcode = generate_fake_postcode()  # Randomized Washington DC postcode
        else:
            zipcode = f'{random.randint(10000, 99999)}-{random.randint(1000, 9999)}'  # Random US postcode
        db.execute(
            'INSERT INTO mechanics (email, name, zipcode, ein, hash) VALUES (?, ?, ?, ?, ?)',
            (email, f'Mechanic {i}', zipcode, '123456789', password)
        )
        if i%10 == 0:
            click.echo(f"MECHANIC: {i}")

    # Populate cars
    car_models = ['Ford Focus', 'Nissan Ultima']
    car_urls = [util.get_car_image("", model) for model in car_models]
    for email in db.execute('SELECT email FROM customers').fetchall():
        registration = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        make_model_url = random.choice(list(zip(car_models, car_urls)))
        db.execute(
            'INSERT INTO cars (registration, owner_email, make, model_number, image_url) VALUES (?, ?, ?, ?, ?)',
            (registration, email['email'], make_model_url[0].split()[0], make_model_url[0].split()[1], make_model_url[1])
        )
        if i%10 == 0:
            click.echo(f"CAR: {i}")

        # Generate fake appointments and reviews for each customer
        generate_fake_appointments(db, email['email'])

    # Commit changes
    db.commit()
    click.echo('Database populated with example customers, cars, and mechanics.')


def init_app(app):
    app.cli.add_command(populate_db_command)
