import unittest
from app import app, db
from models import User, UserMovies, Review

class AppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def setUp(self):
        self.client = self.client
        with app.app_context():
            pass

    def tearDown(self):
        with app.app_context():
            db.session.remove()

    # Basic test to confirm that tests are running
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Replace "Recommendations" with an identifiable text from the HTML template
        self.assertIn(b"Trending Movies", response.data)  # Checking for "Movie Recs" or a similar keyword in the HTML

if __name__ == "__main__":
    unittest.main()
