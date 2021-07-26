import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  def get_categories_dictionary():
    categories = Category.query.all()
    category_dictionary = {}
    for category in categories:
      category_dictionary[category.id] = category.type
    return category_dictionary


  @app.route('/categories')
  def retrieve_categories():
    return jsonify({
      'success': True,
      'categories': get_categories_dictionary()
    })

  '''
  DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [questions.format() for questions in selection]
    current_questions = questions[start:end]

    return current_questions

  @app.route('/questions')
  def retrieve_questions():
    all_questions = Question.query.order_by(Question.id).all()
    current_page_questions = paginate_questions(request, all_questions)

    if len(current_page_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_page_questions,
      'total_questions': len(all_questions),
      'current_category': None,
      'categories': get_categories_dictionary()
    })
  '''
  DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    
    if question is None:
        abort(404)
    
    question.delete()

    return jsonify({
      'success': True,
      'id': question.id
    })

  '''
  DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=["POST"])
  def create_question():

    body = request.get_json()

    new_question = body.get('question')
    new_answer = body.get('answer')
    new_category = body.get('category')
    new_difficulty = body.get('difficulty')
    search_term = body.get('searchTerm')
    
    try:

      if (search_term):
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term)))        
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection.all())
        })
      else:
        new_question = Question(new_question, new_answer, new_category, new_difficulty)
        new_question.insert()

        return jsonify({
          'success': True,
        })

    except:
      abort(422)
  '''
  DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # This is handled in the same endpoint as question creation

  '''
  DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category(category_id):
    category = Category.query.filter(Category.id == category_id).one_or_none()
    
    if category is None:
        abort(404)    
    
    all_questions_for_category = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    current_page_questions = paginate_questions(request, all_questions_for_category)

    if len(current_page_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_page_questions,
      'total_questions': len(all_questions_for_category),
      'current_category': category.type,
      'categories': get_categories_dictionary()
    })

  '''
  DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def next_question():
    body = request.get_json()
    previous_questions_ids = body.get('previous_questions')
    quiz_category = body.get('quiz_category')    

    try:
      quiz_category_id = quiz_category.get('id')
      
      if quiz_category_id == 0:
        all_questions_for_category = Question.query.all()  
      else:
        all_questions_for_category = Question.query.filter(Question.category == quiz_category_id).all()
      
      not_recently_asked = list(filter(lambda q: q.id not in previous_questions_ids, all_questions_for_category))
      
      if len(not_recently_asked) == 0:
        return jsonify({
          'success': True,
          'question': None,
        })
      else: 
        return jsonify({
          'success': True,
          'question': Question.format(random.choice(not_recently_asked)),
        })
    except Exception as err:
      print(err)
      abort(422)

  '''
  DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def on_notfound(error):
    return jsonify({
      'success': False,
      'code': 404,
      'message': 'Entity not found'
    }), 404

  @app.errorhandler(405)
  def on_unsupported_method(error):
    return jsonify({
      'success': False,
      'code': 405,
      'message': 'Method not supported for this endpoint'
    }), 405

  @app.errorhandler(422)
  def on_unprocessable_entity(error):
    return jsonify({
      'success': False,
      'code': 422,
      'message': 'Entity not processable'
    }), 422

  @app.errorhandler(400)
  def on_client_error(error):
    return jsonify({
      'success': False,
      'code': 400,
      'message': 'Client error'
    }), 400

  @app.errorhandler(500)
  def on_server_error(error):
    return jsonify({
      'success': False,
      'code': 500,
      'message': 'Server error. Sorry for the inconvenience.'
    }), 500

  return app

    