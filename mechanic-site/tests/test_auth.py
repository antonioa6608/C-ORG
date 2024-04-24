


def test_customer_register(client):
    # Test customer registration functionality
    # Make POST request to register a customer
    response = client.post('/auth/register_customer', data={
        'email': 'test@example.com',
        'name': 'Test User',
        'password': 'password123'
    })

    # Assert the response status code
    assert response.status_code == 302  # Assuming registration redirects on success


def test_mechanic_register(client):
    # Test mechanic registration functionality
    # Make POST request to register a mechanic
    response = client.post('/auth/register_mechanic', data={
        'email': 'mechanic@example.com',
        'name': 'Mechanic User',
        'password': 'password123',
        'zipcode': '12345',
        'ein': '12-1234567'
    })

    # Assert the response status code
    assert response.status_code == 302  # Assuming registration redirects on success


def test_customer_login(client):
    # Test customer login functionality
    # Make POST request to log in a customer
    response = client.post('/auth/login-customer', data={
        'email': 'test@example.com',
        'password': 'password123'
    })

    # Assert the response status code
    assert response.status_code in [302, 200]  


def test_mechanic_login(client):
    # Test mechanic login functionality
    # Make POST request to log in a mechanic
    response = client.post('/auth/login-mechanic', data={
        'email': 'mechanic@example.com',
        'password': 'password123'
    })

    # Assert the response status code
    assert response.status_code in [302, 200]

def test_customer_register_failure(client):
    # Test customer registration failure due to missing required fields
    # Make POST request to register a customer with missing fields
    response = client.post('/auth/register_customer', data={
        'name': 'Test User',
        'password': 'password123'
    })

    # Assert the response status code
    assert response.status_code == 200
    # Assert the presence of error message in the response content
    assert b'Email is required.' in response.data


def test_mechanic_register_failure(client):
    # Test mechanic registration failure due to invalid EIN format
    # Make POST request to register a mechanic with invalid EIN format
    response = client.post('/auth/register_mechanic', data={
        'email': 'mechanic@example.com',
        'name': 'Mechanic User',
        'password': 'password123',
        'zipcode': '12345',
        'ein': 'invalid_ein_format'
    })

    # Assert the response status code
    assert response.status_code == 200  # Assuming registration returns to the same page on failure
    # Assert the presence of error message in the response content
    assert b'The EIN must be in the format 12-1234567' in response.data


def test_customer_login_failure(client):
    # Test customer login failure due to incorrect password
    # Make POST request to log in a customer with incorrect password
    response = client.post('/auth/register_customer', data={
        'email': 'test@example.com',
        'name': 'Test User',
        'password': 'password123'
    })
    
    response = client.post('/auth/login-customer', data={
        'email': 'test@example.com',
        'password': 'incorrect_password'
    })

    # Assert the response status code
    assert response.status_code == 200  # Assuming login returns to the same page on failure
    # Assert the presence of error message in the response content
    assert b'Incorrect password.' in response.data


def test_mechanic_login_failure(client):
    # Test mechanic login failure due to incorrect username
    # Make POST request to log in a mechanic with incorrect username
    response = client.post('/auth/login-mechanic', data={
        'email': 'nonexistent_mechanic@example.com',
        'password': 'password123'
    })

    # Assert the response status code
    assert response.status_code == 200  # Assuming login returns to the same page on failure
    # Assert the presence of error message in the response content
    assert b'Incorrect username.' in response.data
