from flask import *
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')


#Initialize App
app = Flask(__name__)
app.secret_key = 'drewismyidol'

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
        
        # Initialize empty cart
    if 'cart' not in session:
        session['cart'] = []
        
        # Fetch items from the database  
    items = query_db('SELECT * FROM item')
    return render_template("index.html", items=items)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if not request.json or not request.json['item_id']:
        return jsonify({'success': False})
    item_id = int(request.json['item_id'])  # Using JSON
    if 'cart' not in session:
        session['cart'] = []
    if item_id not in session['cart']:
        session['cart'].append(item_id)
        session.modified = True
    return jsonify({'success': True, 'cart_count': len(session['cart']), 'item_id': item_id})

@app.route('/cart')
def cart():
    cart_items_ids = session.get('cart', [])
    if not cart_items_ids:
        return "Cart is Empty."
    
    id_list = ','.join(str(item_id) for item_id in cart_items_ids)

    query = f"SELECT * FROM item WHERE item_id IN ({id_list})"
    items = query_db(query)
    return render_template("cart.html", items=items)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    session.modified = True
    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(debug=True)
    
