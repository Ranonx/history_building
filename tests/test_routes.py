import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import unittest
from app import app, db, Place, Visited  # Ensure correct imports from your app module

class TestAddVisit(unittest.TestCase):
    def setUp(self):
        # Configure the app to use the testing database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['DEBUG'] = False

        # Establish an application context before running the tests
        self.app_context = app.app_context()
        self.app_context.push()

        # Create all database tables
        db.create_all()

        # Add a test place
        place = Place(file_ref="AM19-0008", name="Test Place", grade="1", district="Test District", address="123 Test St")
        db.session.add(place)
        db.session.commit()

        # Create a test client
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_visit_success(self):
        response = self.client.post('/add-visit', json={'place_id': "AM19-0008"})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Visit added successfully', response.get_data(as_text=True))

    def test_add_nonexistent_place(self):
        response = self.client.post('/add-visit', json={'place_id': "NONEXISTENT"})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_data(as_text=True))

    def test_add_duplicate_visit(self):
        # First visit
        self.client.post('/add-visit', json={'place_id': "AM19-0008"})
        # Duplicate visit
        response = self.client.post('/add-visit', json={'place_id': "AM19-0008"})
        self.assertEqual(response.status_code, 409)
        self.assertIn('Visit already recorded', response.get_data(as_text=True))

    def test_invalid_data_format(self):
        # Sending non-JSON data
        response = self.client.post('/add-visit', data="This is not JSON", content_type='text/plain')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
