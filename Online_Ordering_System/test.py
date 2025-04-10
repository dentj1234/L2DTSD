from flask import Flask, g
import sqlite3

DATABASE = 'database.db'

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

@app.route('/')
def home():
    #Home Page

    db = get_db()
    cursor = db.cursor()
    sql = 'SELECT * FROM item;'
    cursor.execute(sql)
    results = cursor.fetchall()
    return str(results)

if __name__ == "__main__":
    app.run(debug=True)