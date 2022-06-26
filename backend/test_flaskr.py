import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "triviatest"
        self.database_path = "postgresql://{}/{}".format('kazeemadewole@localhost:5433', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.newquestion = {
            "question": "what is my name?",
            "answer":"kazeem",
            "difficulty":4,
            "category": "1"
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["categories"]))
        self.assertEqual(len(data["categories"]), 6)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["sucess"], True)

    def test_get_all_question_for_a_categories(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"], True)
        self.assertTrue(data["currentCategory"], 2)

    def test_delete_question(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["message"])
        self.assertEqual(data["message"], 'deleted')
    #     self.assertTrue(data["sucess"], True)

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.newquestion)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()