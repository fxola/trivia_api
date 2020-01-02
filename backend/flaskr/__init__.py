import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.append("/usr/local/lib/python3.8/site-packages")
from flask_cors import CORS
import random


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def fetch_categories():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    return formatted_categories

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)


  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
      formatted_categories = fetch_categories()
      return jsonify({
        'success':True,
        'categories':formatted_categories
      })
      

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    try:
      page = request.args.get('page',1,type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = Question.query.all()
      response = [question.format() for question in questions]
      categories = fetch_categories()
      return jsonify({
        'success':True,
        'questions':response[start:end],
        'total_questions':len(response),
        'categories': categories,
        'currentCategory':None
      })
    except:
      abort(500)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
      try:
        question = Question.query.filter(Question.id== id).one_or_none()
        if question is None: abort(404)

        question.delete()
        return jsonify({
          "success":True,
          "message":'Question deleted successfully'
        })
      except:
        abort(404)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_questions():
      try:
        body = request.get_json()
        for entry in body.values():
          if(not entry): abort(422)
        
        new_question = Question(question=body['question'],answer=body['answer'],difficulty=body['difficulty'],category=body['category'])
        new_question.insert()
        return jsonify({
          "success":True,
          "message":'Question posted successfully'
        })
      except:
        abort(422)
        
    
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def get_questions_by_search_term():
    try:
      term = request.get_json()['searchTerm']
      if(not term): abort(422)
      page = request.args.get('page',1,type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = Question.query.filter(Question.question.ilike(f'%{term}%')).all()
      response = [question.format() for question in questions]

      return jsonify({
        'success':True,
        'questions':response[start:end],
        'total_questions':len(response),
        'currentCategory':questions[0].category
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_categories(id):
    try:
      page = request.args.get('page',1,type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = Question.query.filter(Question.category== id).all()
      response = [question.format() for question in questions]

      return jsonify({
        'success':True,
        'questions':response[start:end],
        'total_questions':len(response),
        'currentCategory':id
      })
    except:
      abort(500)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    try:
      body = request.get_json()

      if(not term): abort(422)
      page = request.args.get('page',1,type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = Question.query.filter(Question.question.ilike(f'%{term}%')).all()
      response = [question.format() for question in questions]

      return jsonify({
        'success':True,
        'questions':response[start:end],
        'total_questions':len(response),
        'currentCategory':questions[0].category
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False, 
          "error": 404,
          "message": "Not found"
          }), 404

  @app.errorhandler(400)
  def bad_request_error(error):
      return jsonify({
          "success": False, 
          "error": 400,
          "message": "Bad Request"
          }), 400
        
  @app.errorhandler(422)
  def invalid_input_error(error):
      return jsonify({
          "success": False, 
          "error": 422,
          "message": 'Unprocessable Entity'
          }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          "success": False, 
          "error": 500,
          "message": "Internal Server Error"
          }), 500

  return app

    