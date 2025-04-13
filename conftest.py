import pytest
from app import app, create_db, seed_cookies, seed_test_user, drop_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DB_REF'] = 'test_db.sqlite'
    with app.test_client() as client:
        with app.app_context():
            create_db()
            seed_cookies()
            seed_test_user()
        yield client
        with app.app_context():
            drop_db()