'''This version of the example API serves a larger number of results, results that are stored in an SQLite database (books.db). When a 
user requests an entry or set of entries, our API pulls that information from the database by building and executing an SQL query. This 
iteration of our API also allows for filtering by more than one field.'''

# Imports the Flask library, making the code available to the rest of the application.  
# Flask provides us with a jsonify function that allows us to convert lists and dictionaries to JSON format.
# Note that the books.db database file should be located in the same directory as the script itself.
import flask
from flask import request, jsonify
import sqlite3


# app = flask.Flask(__name__) Creates the Flask application object, which contains data about the application and also methods
# (object functions) that tell the application to do certain actions. The last line, app.run(), is one such method.
app = flask.Flask(__name__)


#app.config["DEBUG"] = True — Starts the debugger. With this line, if your code is malformed, you’ll see an error when you visit your app. 
# Otherwise you’ll only see a generic message such as Bad Gateway in the browser when there’s a problem with your code.
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries that exist in the books database catalog. In the route we created, the book entries are 
# converted from a list of Python dictionaries to JSON before being returned to a user. An SQL query is being run against the database in the
# code sample below.

# First, we connect to the database using our sqlite3 library. An object representing the connection to the database is bound to the conn variable. 
# The conn.row_factory = dict_factory line lets the connection object know to use the dict_factory function we’ve defined, which returns items from the
# database as dictionaries rather than lists—these work better when we output them to JSON. We then create a cursor object (cur = conn.cursor()), which
# is the object that actually moves through the database to pull our data. Finally, we execute an SQL query with the cur.execute method to pull out all
# available data (*) from the books table of our database. At the end of our function, this data is returned as JSON: jsonify(all_books). Note that our
# other function that returns data, api_filter, will use a similar approach to pull data from the database.


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)


# In HTML responses, the code 200 means “OK”(the expected data transferred), while the code 404 means “Not Found” 
# (there was no resource available at the URL given). This function allows us to return 404 pages when something goes
# wrong in the application.

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# The function first grabs all the query parameters provided in the URL (remember, query parameters are the part of
# the URL that follows the ?, like ?id=10). It then pulls the supported parameters id, published, and author and binds 
# them to appropriate variables:'''

@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

# The next segment begins to build an SQL query that will be used to find the requested information in the database. 
# SQL queries used to find data in a database take this form: 
# `SELECT <columns> FROM <table> WHERE <column=match> AND <column=match>;


    query = "SELECT * FROM books WHERE"
    to_filter = []

# Then, if id, published, or author were provided as query parameters, we add them to both the query and the filter list.
# If the user has provided none of these query parameters, we have nothing to show, so we send them to the “404 Not Found” page.

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

# To perfect our query, we remove the trailing ` AND and cap the query with the ;` required at the end of all SQL statements.

    query = query[:-4] + ';'

# Finally, we connect to our database as in our api_all function, then execute the query we’ve built using our filter list.

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

# We return the results of our executed SQL query as JSON to the user.

    return jsonify(results)

app.run()



# After running the script and launcing the flask APP, API queries against the books.db can be made by using the examples below.
# http://127.0.0.1:5000/api/v1/resources/books/all 
# http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis 
# http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis&published=1999 
# http://127.0.0.1:5000/api/v1/resources/books?published=2010
