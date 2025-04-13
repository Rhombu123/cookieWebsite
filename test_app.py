def test_profile(client, setup_db):
    with client:
        # Simulate logging in
        client.post('/login', data={'email': 'test@example.com', 'password': 'hashedpassword'})

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
