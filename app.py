from flask import Flask, render_template, request
import sqlite3
import base64
from hashlib import sha256

def hash_password(password):
    encoded_string = password.encode('utf-8')
    encoded_hash = base64.b64encode(sha256(encoded_string).digest())
    return encoded_hash.decode()

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

@app.route('/create_user', methods = ['POST', 'GET'])
def create_user():
    try:
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone = request.form['phone']
        newsletter = request.form['newsletter']

        if password != confirm_password:
            return render_template('signup.html', msg='Passwords do not match')

        with sqlite3.connect('db.sqlite') as conn:
            password_hash = hash_password(password)

            cursor = conn.cursor()
            cursor.execute('''
                        INSERT INTO users (
                            first_name, last_name, email, password_hash, phone_number, gets_newsletters
                        ) VALUES (?,?,?,?,?,?)''', (first_name, last_name, email, password_hash, phone, newsletter))
            conn.commit()
            target = 'thank_you.html'
            msg = ''
    except Exception as e:
        conn.rollback()
        target = 'signup.html'
        # msg = 'An internal error occurred while processing your request'
        msg = 'Error: ' + str(e)
    finally:
        conn.close()
        return render_template(target, msg=msg)


@app.route('/signup')
def signup():
    return render_template('signup.html', msg='')

def create_db():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT,
                        password_hash TEXT,
                        phone_number TEXT CAN BE NULL,
                        gets_newsletters BIT
                    );
                    ''')
    conn.commit()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cookies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        description TEXT,
                        price REAL,
                        image_url TEXT,
                        category TEXT
                    );
                    ''')
    conn.commit()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cart_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        cookie_id INTEGER,
                        quantity INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (cookie_id) REFERENCES cookies (id)
                    );
                    ''')
    conn.commit()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        cookie_id INTEGER,
                        quantity INTEGER,
                        total_price REAL,
                        order_date DATETIME,
                        status TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (cookie_id) REFERENCES cookies (id)
                    );
                    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
