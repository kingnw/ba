import unittest
from app import app, db  # Ensure you're importing the app with blueprints registered
from models import User, UserMovies

class WatchlistFavoritesTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Configure the app for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

        # Create the test client
        self.client = app.test_client()

        # Create the database and tables
        with app.app_context():
            db.create_all()
            # Create a test user using the application's user creation method
            self.test_username = "testuser" + str(id(self))
            self.test_password = "testpassword"
            self.user = User.create_user(self.test_username, self.test_password)
            self.user_id = self.user.id  # Store the user ID

    def login(self):
        """Helper method to log in the test user."""
        response = self.client.post('/auth/login', data=dict(
            username=self.test_username,
            password=self.test_password
        ), follow_redirects=True)
        
        # Assert that the login was successful by checking for a success message
        self.assertIn(b'Logged in successfully.', response.data)
        self.assertEqual(response.status_code, 200)
        
        # Optionally, verify that the user is marked as authenticated in the session
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['_user_id'], str(self.user_id))
        
        return response

    def test_add_movie_to_watchlist(self):
        """Test adding a movie to the watchlist."""
        with self.client:
            # Log in the user
            self.login()

            movie_id = 1
            response = self.client.post(f'/watchlist/add/{movie_id}', follow_redirects=True)

            # Check if the response is successful
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Movie added to watchlist.", response.data)

            with app.app_context():
                user_movie = UserMovies.query.filter_by(
                    user_id=self.user_id, movie_id=movie_id, category='watchlist'
                ).first()
                self.assertIsNotNone(user_movie)

    def test_remove_movie_from_watchlist(self):
        """Test removing a movie from the watchlist."""
        with self.client:
            # Log in the user
            self.login()

            movie_id = 1
            # First, add the movie to the watchlist
            add_response = self.client.post(f'/watchlist/add/{movie_id}', follow_redirects=True)
            self.assertEqual(add_response.status_code, 200)
            self.assertIn(b"Movie added to watchlist.", add_response.data)

            # Now, remove the movie from the watchlist
            remove_response = self.client.post(f'/watchlist/remove/{movie_id}', follow_redirects=True)

            # Check if the response is successful
            self.assertEqual(remove_response.status_code, 200)
            self.assertIn(b"Movie removed from watchlist.", remove_response.data)

            with app.app_context():
                user_movie = UserMovies.query.filter_by(
                    user_id=self.user_id, movie_id=movie_id, category='watchlist'
                ).first()
                self.assertIsNone(user_movie)

    def test_add_movie_to_favorites(self):
        """Test adding a movie to the favorites."""
        with self.client:
            # Log in the user
            self.login()

            movie_id = 1
            response = self.client.post(f'/favorites/add/{movie_id}', follow_redirects=True)

            # Check if the response is successful
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Movie added to favorites.", response.data)

            with app.app_context():
                user_movie = UserMovies.query.filter_by(
                    user_id=self.user_id, movie_id=movie_id, category='favorites'
                ).first()
                self.assertIsNotNone(user_movie)

    def test_remove_movie_from_favorites(self):
        """Test removing a movie from the favorites."""
        with self.client:
            # Log in the user
            self.login()

            movie_id = 1
            # First, add the movie to the favorites
            add_response = self.client.post(f'/favorites/add/{movie_id}', follow_redirects=True)
            self.assertEqual(add_response.status_code, 200)
            self.assertIn(b"Movie added to favorites.", add_response.data)

            # Now, remove the movie from the favorites
            remove_response = self.client.post(f'/favorites/remove/{movie_id}', follow_redirects=True)

            # Check if the response is successful
            self.assertEqual(remove_response.status_code, 200)
            self.assertIn(b"Movie removed from favorites.", remove_response.data)

            with app.app_context():
                user_movie = UserMovies.query.filter_by(
                    user_id=self.user_id, movie_id=movie_id, category='favorites'
                ).first()
                self.assertIsNone(user_movie)

    def test_view_watchlist(self):
        """Test viewing the watchlist."""
        with self.client:
            # Log in the user
            self.login()

            movie_id = 1
            # Add a movie to the watchlist
            add_response = self.client.post(f'/watchlist/add/{movie_id}', follow_redirects=True)
            self.assertEqual(add_response.status_code, 200)
            self.assertIn(b"Movie added to watchlist.", add_response.data)

            # View the watchlist
            response = self.client.get('/watchlist')

            # Check if the response is successful
            self.assertEqual(response.status_code, 200)

            # Check if the movie is present in the watchlist
            with app.app_context():
                user_movies = UserMovies.query.filter_by(
                    user_id=self.user_id, category='watchlist'
                ).all()
                self.assertTrue(len(user_movies) > 0)
                self.assertEqual(user_movies[0].movie_id, movie_id)

            # Optionally check for specific content in response.data
            # self.assertIn(b"Expected content", response.data)

    def test_view_favorites(self):
        """Test viewing the favorites."""
        with self.client:
            # Log in the user
            self.login()

            movie_id = 1
            # Add a movie to the favorites
            add_response = self.client.post(f'/favorites/add/{movie_id}', follow_redirects=True)
            self.assertEqual(add_response.status_code, 200)
            self.assertIn(b"Movie added to favorites.", add_response.data)

            # View the favorites
            response = self.client.get('/favorites')

            # Check if the response is successful
            self.assertEqual(response.status_code, 200)

            # Check if the movie is present in the favorites
            with app.app_context():
                user_movies = UserMovies.query.filter_by(
                    user_id=self.user_id, category='favorites'
                ).all()
                self.assertTrue(len(user_movies) > 0)
                self.assertEqual(user_movies[0].movie_id, movie_id)

            # Optionally check for specific content in response.data
            # self.assertIn(b"Expected content", response.data)

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()

# Problem: Your tests are attempting to make real HTTP requests to an external service (api.themoviedb.org). 
# This is generally not recommended for unit tests because:
# Flakiness: Tests become dependent on external services' availability and response times.
# Performance: Real HTTP requests can significantly slow down your test suite.
# Security: Exposing API keys in test outputs can be a security risk.
# SSL Errors:
# Cause: The SSL error suggests that the connection to the external API was abruptly closed or couldn't 
# be established correctly during the SSL handshake. This could be a transient network issue, 
# but in the context of testing, it's more likely due to the aforementioned reasons.
