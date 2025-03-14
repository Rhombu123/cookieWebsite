import os

from flask import Flask, render_template, request, redirect, url_for, session,flash
import sqlite3
import base64
from hashlib import sha256
import csv

def hash_password(password):
    encoded_string = password.encode('utf-8')
    encoded_hash = base64.b64encode(sha256(encoded_string).digest())
    return encoded_hash.decode()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_PERMANENT'] = False

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

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)  # Remove the cart key from the session
    flash("Cart has been cleared.", "info")
    return redirect(url_for('cart'))

@app.before_request
def clear_cart_on_first_visit():
    # Check if a specific key in the session indicates the user has visited before.
    if 'app_first_run' not in session:
        session.pop('cart', None)
        session['app_first_run'] = True
        session.modified = True

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'first_name' not in session:
        flash("You need to log in before adding items to the cart.", "danger")
        return redirect(url_for('login'))

    # Get item details from the POST request
    cookie_name = request.form.get('cookie_name')
    cookie_price = float(request.form.get('cookie_price'))
    quantity = int(request.form.get('quantity', 1))

    # Retrieve cart from session or initialize it
    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    # Check if the item already exists in the cart, update quantity if true
    item_found = False
    for item in cart:
        if item['name'] == cookie_name:
            item['quantity'] += quantity
            item_found = True
            break

    if not item_found:
        # Add new item to the cart
        cart.append({
            'name': cookie_name,
            'price': cookie_price,
            'quantity': quantity
        })

    # Save the updated cart back to session
    session['cart'] = cart
    flash(f"{cookie_name} added to your cart!", "success")
    return redirect(url_for('products'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        email= request.form['email']
        password = request.form['password']
        password_hash = hash_password(password)
        with sqlite3.connect('db.sqlite') as con:
            cursor = con.cursor()
            cursor.execute('SELECT first_name, last_name FROM users WHERE email = ? AND password_hash = ?',
                           (email, password_hash))
            user = cursor.fetchone()

        if user:
             # User found, store user details in session
             session['first_name'] = user[0]
             session['last_name'] = user[1]
             print(f"Session data; {session}")
             return redirect(url_for('welcome'))  # Redirect to a welcome page
        else:
            flash('Invalid email or password', 'danger')
            return render_template('login.html')

    return render_template('login.html')
@app.route('/welcome')
def welcome():
    if 'first_name' in session and 'last_name' in session:
       # Retrieve data from session
        first_name = session['first_name']
        last_name = session['last_name']
       # Pass them to the template
        return render_template("welcome.html", first_name=first_name, last_name=last_name)

    return redirect(url_for('login'))  # Redirect to login if no session exists

@app.route('/cart')
def cart():
   if 'cart' not in session or not session['cart']:
       # Empty cart
        return render_template('cart.html', cart_items=[], total=0)

   cart_items = session['cart']
   # Calculate total cost
   total = sum(item['price'] * item['quantity'] for item in cart_items)

   return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    return render_template('checkout.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Process the form data here
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    address = request.form.get('address')
    payment_method = request.form.get('payment_method')

    # Add logic for saving data or processing payment here
    return render_template('thank_you_for_order.html', email=email)


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

# DANGER: USE SPARINGLY! Make sure to clean up any lingering foreign keys before using this
def reset_cookies():
    try:
        with sqlite3.connect("db.sqlite") as conn:
            cursor = conn.cursor()

            cursor.execute('''DELETE FROM cookies''')
            conn.commit()
    except Exception as e:
        conn.rollback()
        print("Failed to purge cookies table: " + str(e))
    finally:
        conn.close()

def read_csv():
    try:
        with open("cookies_table.csv", 'r') as file_reader:
            reader = csv.reader(file_reader)
            output = list(reader)
    except Exception as e:
        print("Error processing cookies_table.csv: " + str(e))
        output = []
    finally:
        file_reader.close()
        return output

def seed_cookies():
    try:
        with sqlite3.connect("db.sqlite") as conn:
            cursor = conn.cursor()

            cursor.execute('''SELECT COUNT(*) FROM cookies''')
            conn.commit()

            result = cursor.fetchone()

            count = int(result[0])

            if count <= 0:
                cookies = read_csv()
                if len(cookies) > 0:
                    for name, desc, price, img_url, cat in cookies:
                        cursor.execute('''
                                        INSERT INTO cookies (
                                            name, description, price, image_url, category
                                        ) VALUES (?,?,?,?,?); ''', [name, desc, price, img_url, cat])
                        conn.commit()
                    print("Cookies seeded")
                else:
                    print("No cookies to seed")
            else:
                print("Cookies already seeded")
    except Exception as e:
        conn.rollback()
        print("Error seeding cookies: " + str(e))
    finally:
        conn.close()

if __name__ == '__main__':
    create_db()
    # reset_cookies()
    seed_cookies()
    app.run(debug=True)
