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

def query_db(query):
    cur = get_db().execute(query)
    result = cur.fetchall()
    cur.close()
    return result

@app.route('/menu')
def menu():
    #Menu Page
    items = query_db('SELECT * FROM item')
    return render_template("index.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)
    