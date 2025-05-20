from flask import *
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')

#Initialize App
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
    #Home Page
    return render_template("index.html")

    #sql = 'SELECT * FROM item;'
    #results = query_db(sql)
    #return str(results)

@app.route('/api/getmenu')
def menu():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True)