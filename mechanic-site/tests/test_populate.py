from mechanic_site.populate import generate_fake_postcode, generate_fake_email, populate_db_command


from mechanic_site.db import get_db
from click.testing import CliRunner

"""def test_populate_db_command(app):

    with app.app_context():
        populate_db_command()

        db = get_db()
        cursor = db.cursor()

        # Check if the customers table is populated
        cursor.execute("SELECT COUNT(*) FROM customers")
        assert cursor.fetchone()[0] == 899  # Expected number of customers

        # Check if the mechanics table is populated
        cursor.execute("SELECT COUNT(*) FROM mechanics")
        assert cursor.fetchone()[0] == 400  # Expected number of mechanics

        # Check if the cars table is populated
        cursor.execute("SELECT COUNT(*) FROM cars")
        assert cursor.fetchone()[0] == 899  # Expected number of cars

        # Check if the appointments table is populated
        cursor.execute("SELECT COUNT(*) FROM appointments")
        assert cursor.fetchone()[0] > 0  # Expected appointments to be present

        # Close the database connection
        cursor.close()
"""

def test_generate_fake_postcode():
    # Test the generate_fake_postcode function
    postcode = generate_fake_postcode()
    
    # Assert that the generated postcode is a string
    assert isinstance(postcode, str)
    # Assert that the generated postcode has the correct format
    assert len(postcode) in [5, 10]
    assert postcode.count('-') <= 1
    assert postcode.replace('-', '').isdigit()

def test_generate_fake_email():
    # Test the generate_fake_email function
    email = generate_fake_email("testing", 1)
    
    # Assert that the generated email is a string
    assert isinstance(email, str)
    # Assert that the generated email has the correct format
    assert '@' in email
    assert '.' in email.split('@')[-1]
    assert len(email.split('@')[0]) > 0
    assert len(email.split('@')[-1].split('.')[0]) > 0
    assert len(email.split('@')[-1].split('.')[1]) > 0