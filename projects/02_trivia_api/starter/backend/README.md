# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 





## API Endpoints documentation

```
GET /categories

- Retrieves all the available categories in a dictionary object. The keys are the ids of the categories, the values are their names (database field `type`).
- Response body: 
{
    'categories': {
        str: str,
        ...
    }
}
```

```
GET /questions

- Retrieves all the questions in a paginated fashion. Each page contains max 10 questions. The total number of available questions is always returned. The category dictionary is returned here as in `/categories`. `current_category` is always null for this endpoint.
- query param `page`: the page number. Defaults to 1.
- Response body: 
{
    'success': bool,
    'questions': [
        {
            'id': int,
            'question': str,
            'answer': str,
            'category': int,
            'difficulty': int
        },
        ..
    ],
    'total_questions': int,
    'current_category': null, // always null for this endpoint
    'categories': {
        str: str,
        ...
    }
}
```
```
DELETE /quesitons/{id}
- Deletes a specific question, identified by the parameter `id`.
- path argument `id`: the question to be deleted. Can't be null.
- Response body:
{
    'success': bool,
    'id': int
}
```
```
POST /questions
Creates a new question or searches for questions containing a search string.
- body argument `searchTerm`: the search term, as a string. If given, a paginated list of questions containing the search string will be returned. If missing, a new question will be created with the values contained in the other arguments.
- body argument `question`: The question (string).
- body argument `answer`: The answer to the given question (string).
- body argument `category`: The id of the category this question belongs to (int).
- body argument `difficulty`: The difficulty of this question (int).
- query param `page`: the page number. Defaults to 1. Only applies to search.
- Response body for search: 
{
    'success': bool,
    'questions': [
        {
            'id': int,
            'question': str,
            'answer': str,
            'category': int,
            'difficulty': int
        },
        ..
    ],
    'total_questions': int
}
- Response body for create: 
{
    'success': bool
}
```
```
GET categories/{category_id}/questions

- Retrieves all the questions for the given category in a paginated fashion. Each page contains max 10 questions. The total number of available questions in the given category is always returned. The category dictionary is returned here as in `/categories`. `current_category` is the name of the choosen category.
- path argument `category_id`: The id for the choosen category. Can't be null.
- query param `page`: the page number. Defaults to 1.
- Response body: 
{
    'success': bool,
    'questions': [
        {
            'id': int,
            'question': str,
            'answer': str,
            'category': int,
            'difficulty': int
        },
        ..
    ],
    'total_questions': int,
    'current_category': str,
    'categories': {
        str: str,
        ...
    }
}
```
```
POST /quizzes
Given a category and a list of ids of already asked questions, returns a random new question of the given category. If all questions for the category have been asked, returns null to signal the end of the game.
- body argument `previous_questions`: The list of already answered questions' ids ([int]).
- body argument `quiz_category`: The id for the category we are playing with (int).
- Response body:
{
    'success': bool,
    'question': {
            'id': int,
            'question': str,
            'answer': str,
            'category': int,
            'difficulty': int
    } || null
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
