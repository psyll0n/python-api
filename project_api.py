# Imports the Flask library, making the code available to the rest of the application.  
# Flask provides us with a jsonify function that allows us to convert lists and dictionaries to JSON format.
import flask
from flask import request, jsonify


# app = flask.Flask(__name__) Creates the Flask application object, which contains data about the application and also methods
# (object functions) that tell the application to do certain actions. The last line, app.run(), is one such method.
app = flask.Flask(__name__)

#app.config["DEBUG"] = True — Starts the debugger. With this line, if your code is malformed, you’ll see an error when you visit your app. 
# Otherwise you’ll only see a generic message such as Bad Gateway in the browser when there’s a problem with your code.
app.config["DEBUG"] = True


# The books list below contains some test data for a catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


# A route to return all of the available entries that exist in the books catalog. In the route we created, the book entries are 
# converted from a list of Python dictionaries to JSON before being returned to a user.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


# In this code, we first create a new function, called api_id, with the @app.route syntax that maps the function to the path 
# /api/v1/resources/books
@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    if 'id' in request.args:
        id = int(request.args['id'])
    # Note that accessing the URL link: http://127.0.0.1:5000/api/v1/resources/book without providing an ID will give an error message.
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Examine the provided URL for an id and select the books that match that id. The id must be provided like this: ?id=0. 
    # Data passed through URLs like this (after the ?) are called query parameters
    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results.
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

# A method that runs the application server.
app.run()

# Once the server is running, visit our route URL to view the data in the catalog:
# http://127.0.0.1:5000/api/v1/resources/books/all

# API get requests can be run against the web app by navigating to the following URL addresses:

# 127.0.0.1:5000/api/v1/resources/books?id=0 
# 127.0.0.1:5000/api/v1/resources/books?id=1 
# 127.0.0.1:5000/api/v1/resources/books?id=2 
# 127.0.0.1:5000/api/v1/resources/books?id=3