import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # cors = CORS(app, resources={r"/api/*": {origins: "*"}})
    cors = CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-control-Allow-Methods', 'POST, GET, PUT, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_all_categories():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * 10
            end = start + 10
            categories = Category.query.all()
            if start > len(categories):
                abort(404)
            formatted_categories = {}
            for category in categories:
                formatted_categories[category.id] = category.type
            return jsonify({
                'sucess': True,
                'categories' : formatted_categories,
                'total_categories': len(formatted_categories)
            })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_all_questions():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * 10
            end = start + 10
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]
            if start > len(formatted_questions):
                abort(404)
            categories = Category.query.all()
            formatted_categories = {}
            for category in categories:
                formatted_categories[category.id] = category.type
            return jsonify({
                'sucess': True,
                'questions' : formatted_questions[start:end],
                'categories': formatted_categories,
                'total_questions': len(formatted_questions)
            })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_single_question(question_id):
        try:
            question = Question.query.get(question_id)
            db.session.delete(question)
            db.session.commit()
            return jsonify({
            'sucess': True,
            'message' : 'deleted',
            'question_id': question_id
        })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        try: 
            body = request.get_json()
            question = Question(body["question"],body["answer"], body["category"],body["difficulty"])
            question.insert()
            return jsonify({
            'sucess': True
            })   
        except:        
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try: 
            body = request.get_json()
            if body["searchTerm"]:
                questions = Question.query.filter(Question.question.ilike('%'+body["searchTerm"]+'%')).all()
                if len(questions) == 0:
                    abort(404)
                formatted_questions = [question.format() for question in questions]
                categories = Category.query.all()
                formatted_categories = {}
                for category in categories:
                    formatted_categories[category.id] = category.type
                return jsonify({
                'sucess': True,
                'questions' : formatted_questions,
                'categories': formatted_categories,
                'total_questions': len(formatted_questions)
                })
        except:        
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * 10
            end = start + 10
            questions = Question.query.filter_by(category=category_id).all()
            if len(questions) == 0:
                abort(404)
            formatted_question = [question.format() for question in questions]
            return jsonify({
            'sucess': True,
            'questions' : formatted_question[start:end],
            'totalQuestions': len(formatted_question),
            'currentCategory': category_id
            })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try: 
            body = request.get_json()
            questions = Question.query.filter_by(category=body["quiz_category"]).all()
            rand = random.randint(0,len(questions)+1)
            formatted_question = [question.format() for question in questions]
            return jsonify({
            'sucess': True,
            'question':formatted_question[rand]
            })   
        except:        
            db.session.rollback()
            return jsonify({
            'sucess': False
            }) 
        finally:
            db.session.close()
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "sucess": False,
            "error": 404,
            "message": "Not found"
        }),404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'sucess': False,
            'error': 422,
            'message': "unprocessable"
        }),422

    return app

