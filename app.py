from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/shipping')
def shipping():
    return render_template('shipping.html')

@app.route('/wholesale')
def wholesale():
    return render_template('wholesale.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cart')
def cart():
    # This is a placeholder - you'll need to implement actual cart functionality
    cart_items = []  # This will come from your database or session
    cart_count = len(cart_items)
    return render_template('cart.html', cart_items=cart_items, cart_count=cart_count)

@app.route('/signup')
def signup():
    return render_template('signup.html')

def create_db():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT,
                        password TEXT,
                        phone_number TEXT CAN BE NULL,
                        gets_newsletters BIT
                        )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
