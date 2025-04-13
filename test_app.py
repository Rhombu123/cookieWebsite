def test_signup(client):
    response = client.post('/create_user', data={'first-name': 'John', 'last-name': 'Doe', 'email': 'test@example.com', 'password': 'hashedpassword', 'confirm-password': 'hashedpassword', 'phone': '000-000-0000', 'newsletter': 'False'})

    assert response.status_code == 200
    assert b'Thank You' in response.data

def test_login(client):
    # test login response
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'hashedpassword'})

    assert response.status_code == 302
    # test proper session cookie usage
    response = client.get('/welcome')

    assert response.status_code == 200

def test_profile(client):
    # Simulate logging in
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'hashedpassword'})

    assert response.status_code == 302
    # Access the profile page
    response = client.get('/profile')
    assert b'Your Profile' in response.data
    assert b'Order History' in response.data

    # Update profile data
    response = client.post('/update_profile', data={
        'first_name': 'Updated',
        'last_name': 'User',
        'email': 'updated@example.com',
        'phone': '123456789',
        'newsletter': 'on'
    })
    assert b'Profile updated successfully!' in response.data

def test_cart(client):
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'hashedpassword'})

    assert response.status_code == 302

    response = client.post('/add_to_cart', data={'cookie_name': 'Chocolate Chip', 'cookie_price': 1.00, 'quantity': 12})

    assert response.status_code == 302

    response = client.post('/process_payment', data={'full_name': 'John Doe', 'email': 'test@example.com', 'address': '1234 Example Street, My City, My State', 'payment_method': 'Credit Card'})

    assert response.status_code == 200

    response = client.get('/clear_cart')

    assert response.status_code == 302

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

