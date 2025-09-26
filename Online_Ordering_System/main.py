from flask import *
from collections import Counter
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

# Menu Page Route
@app.route('/menu')
def menu():
        # Create a cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
        
        # Fetch items from the database and passes the items to main.html to display
    items = query_db('SELECT * FROM item')
    return render_template("menu.html", items=items)

@app.route('/home')
def home():
        # Create a cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
        
        # Fetch items from the database and passes the items to home.html to display
    items = query_db('SELECT * FROM item')
    return render_template("home.html", items=items)

# Add to cart route used by javascript to add items to the cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    #Check if the request contains JSON data and has an item_id
    if not request.json or not request.json['item_id']:
        return jsonify({'success': False})
    item_id = int(request.json['item_id'])  # Using JSON
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(item_id)
    session.modified = True
    return jsonify({'success': True, 'cart_count': len(session['cart']), 'item_id': item_id})

# Cart Page Route
@app.route('/cart') 
def cart():
    cart_items_ids = session.get('cart', [])
    counts = Counter(cart_items_ids)

    if not cart_items_ids:
        return render_template("cart.html", items=[], counts=counts, total=0)
    
    id_list = ','.join(str(item_id) for item_id in counts.keys())
    query = f"SELECT * FROM item WHERE item_id IN ({id_list})"
    items = query_db(query)
    
    items_with_qty = []
    for item in items:
        items_with_qty.append({
            'item_id': item[0],
            'name': item[2],
            'price': item[3],
            'qty': counts[item[0]]
        })
    total = 0
    for item in items:
        qty = counts[item[0]]
        total += qty * item[3]
    
    return render_template("cart.html", items=items, counts=counts, total=total)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    session.modified = True
    return jsonify({'success': True})

@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.get_json() or {}
    # accept either item_id or id
    item_id = data.get('item_id') or data.get('id')
    quantity = data.get('quantity')

    try:
        item_id = int(item_id)
        quantity = int(quantity)
    except (TypeError, ValueError):
        return jsonify(success=False), 400

    # cart is a list of item ids
    cart = session.get('cart', [])

    # remove existing instances of the item
    cart = [i for i in cart if i != item_id]

    # add the item quantity times (if qty > 0)
    if quantity > 0:
        cart.extend([item_id] * quantity)

    session['cart'] = cart
    session.modified = True
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)

    