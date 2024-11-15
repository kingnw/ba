import unittest
from app import app, db
from models import User

class TemplateTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_login(self):
        """Test the user login functionality."""
        with app.app_context():
            # Check if the user already exists
            if not User.get('testuser'):
                User.create_user(username='testuser', password='password123')  # Create user only if not exists

        # Test login functionality
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password123'  # Login with correct password
        }, follow_redirects=True)

        # Assert response status code and flash message
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Logged in successfully.", response.data)


if __name__ == '__main__':
    unittest.main()
