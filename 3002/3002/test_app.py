import unittest
from app import app, db
class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
        self.client = app.test_client()  # Test client for sending requests
        with app.app_context():
            db.create_all()  # Create database schema

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables

    def test_registration_missing_fields(self):
        # Test missing username
        response = self.client.post('/auth/register', data={
            'username': '',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Username is required.", response.data)

        # Test missing password
        response = self.client.post('/auth/register', data={
            'username': 'testuser',
            'password': ''
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password is required.", response.data)

    def test_successful_registration(self):
        # Test successful registration
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registration successful.", response.data)

    def test_duplicate_username(self):
        # Register a user
        self.client.post('/auth/register', data={
            'username': 'existinguser',
            'password': 'password123'
        }, follow_redirects=True)

        # Attempt to register with the same username
        response = self.client.post('/auth/register', data={
            'username': 'existinguser',
            'password': 'newpassword123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Username already exists.", response.data)

        


    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Trending Movies", response.data)



  
if __name__ == '__main__':
    unittest.main()
