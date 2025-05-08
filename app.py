
"""
app.py

Main Flask web application for a cookie store.
Handles routing, user authentication,
cart management, checkout, and database operations.
"""

import os
import sqlite3
from sqlite3 import DatabaseError
import base64
from hashlib import sha256
import csv

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask import flash

def hash_password(password):
    """Hashes a password using SHA-256 and encodes it in base64."""
    encoded_string = password.encode('utf-8')
    encoded_hash = base64.b64encode(sha256(encoded_string).digest())
    return encoded_hash.decode()


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.config['DB_REF'] = 'db.sqlite'


@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')


@app.route('/products')
def products():
    """Render the products page."""
    return render_template('products.html')


@app.route('/shipping')
def shipping():
    """Render the shipping information page."""
    return render_template('shipping.html')


@app.route('/wholesale')
def wholesale():
    """Render the wholesale information page."""
    return render_template('wholesale.html')


@app.route('/contact')
def contact():
    """Render the contact page."""
    return render_template('contact.html')


@app.route('/clear_cart')
def clear_cart():
    """Clear the user's shopping cart from the session."""
    session.pop('cart', None)  # Remove the cart key from the session
    flash("Cart has been cleared.", "info")
    return redirect(url_for('cart'))


@app.before_request
def clear_cart_on_first_visit():
    """Clears the cart when the session starts for the first time."""
    if 'app_first_run' not in session:
        session.pop('cart', None)
        session['app_first_run'] = True
        session.modified = True


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Adds a cookie to the user's shopping cart stored in the session."""
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

    newcart = session['cart']

    # Check if the item already exists in the cart, update quantity if true
    item_found = False
    for item in newcart:
        if item['name'] == cookie_name:
            item['quantity'] += quantity
            item_found = True
            break

    if not item_found:
        # Add new item to the cart
        newcart.append({
            'name': cookie_name,
            'price': cookie_price,
            'quantity': quantity
        })

    # Save the updated cart back to session
    session['cart'] = newcart
    flash(f"{cookie_name} added to your cart!", "success")
    return redirect(url_for('products'))


@app.route('/profile_old')
def profile_old():
    """Displays an old version of the user's profile page."""
    if 'first_name' not in session or 'last_name' not in session:
        flash(
            "You need to log in to view your profile.",
            "danger")
        return redirect(url_for('login'))

    user_first_name = session['first_name']
    user_last_name = session['last_name']

    with sqlite3.connect(app.config['DB_REF']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT first_name, last_name, email, phone_number, gets_newsletters
            FROM users
            WHERE first_name = ? AND last_name = ?;
        ''', (user_first_name, user_last_name))
        user_details = cursor.fetchone()

    return render_template('profile.html', user_details=user_details)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    """Updates the user's profile information in the database."""
    if 'first_name' not in session or 'last_name' not in session:
        flash(
            "You need to log in to update your profile.",
            "danger")
        return redirect(url_for('login'))

    # Get updated profile details from the form
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    newsletter = 1 if request.form.get('newsletter') else 0

    # Update the user information in the database
    with sqlite3.connect(app.config['DB_REF']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET first_name = ?, last_name = ?, email = ?, phone_number = ?,
             gets_newsletters = ?
            WHERE first_name = ?
            AND last_name = ?;
        ''', (first_name, last_name, email, phone, newsletter,
              session['first_name'], session['last_name']))
        conn.commit()

    # Update the session data with the new name
    session['first_name'] = first_name
    session['last_name'] = last_name

    flash("Profile updated successfully!", "success")
    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    """Displays the logged-in user's profile and order history."""
    if 'first_name' not in session or 'last_name' not in session:
        flash("You need to log in to view your profile.", "danger")
        return redirect(url_for('login'))

    user_first_name = session['first_name']
    user_last_name = session['last_name']

    with sqlite3.connect(app.config['DB_REF']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT first_name, last_name, email, phone_number, gets_newsletters
            FROM users
            WHERE first_name = ? AND last_name = ?;
        ''', (user_first_name, user_last_name))
        user_details = cursor.fetchone()

        # Fetch order history
        cursor.execute('''
            SELECT o.id, o.order_date, o.total_price, o.status
            FROM orders o
            JOIN users u ON u.id = o.user_id
            WHERE u.first_name = ? AND u.last_name = ?
            ORDER BY o.order_date DESC;
        ''', (user_first_name, user_last_name))
        orders = cursor.fetchall()

    return render_template('profile.html',
                           user_details=user_details, orders=orders)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticates a user and sets session data."""
    if request.method == 'POST':
        print(request.form)
        email = request.form['email']
        password = request.form['password']
        password_hash = hash_password(password)
        with sqlite3.connect(app.config['DB_REF']) as con:
            cursor = con.cursor()
            cursor.execute('SELECT first_name, last_name '
                           'FROM users WHERE email = ? AND password_hash = ?',
                           (email, password_hash))
            user = cursor.fetchone()

        if user:
            # User found, store user details in session
            session['first_name'] = user[0]
            session['last_name'] = user[1]
            print(f"Session data; {session}")
            return redirect(url_for('profile'))  # Redirect to profile page

        flash('Invalid email or password', 'danger')
        return render_template('login.html')

    return render_template('login.html')


@app.route('/welcome')
def welcome():
    """Displays a welcome message if the user is logged in."""
    if 'first_name' in session and 'last_name' in session:
        # Retrieve data from session
        first_name = session['first_name']
        last_name = session['last_name']
        # Pass them to the template
        return render_template("welcome.html",
                               first_name=first_name, last_name=last_name)

    return redirect(url_for('login'))  # Redirect to login if no session exists


@app.route('/cart')
def cart():
    """Displays the user's cart and calculates total cost."""
    if 'cart' not in session or not session['cart']:
        # Empty cart
        return render_template('cart.html', cart_items=[], total=0)

    cart_items = session['cart']
    # Calculate total cost
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Displays the checkout form."""
    cart_items = session.get('cart', [])
    total = sum(item["price"] * item['quantity'] for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)


@app.route('/process_payment', methods=['POST'])
def process_payment():
    """Processes the user's payment, creates an order,
     and clears the cart upon successful transaction."""
    # Ensure the user is logged in
    if 'first_name' not in session or 'last_name' not in session:
        flash("Please log in to complete your order.", "danger")
        return redirect(url_for('login'))

    # Get the form data
    form_data = {
        'full_name': request.form.get('full_name'),
        'email': request.form.get('email'),
        'address': request.form.get('address'),
        'payment_method': request.form.get('payment_method')
    }

    # Retrieve cart items
    cart_items = session.get('cart', [])
    if not cart_items:
        flash("Your cart is empty.", "danger")
        return redirect(url_for('cart'))

    # Calculate total price
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = 'Pending'

    try:
        with sqlite3.connect(app.config['DB_REF']) as conn:
            cursor = conn.cursor()

            # Get user ID
            user_id = get_user_id(session['first_name'],
                                  session['last_name'], cursor)
            if not user_id:
                flash("User not found.", "danger")
                return redirect(url_for('login'))

            # Create order and add items to order_items table
            order_id = create_order(user_id, total, order_date, status, cursor)
            add_items_to_order(cart_items, order_id, cursor)

            conn.commit()

        session['cart'] = []  # Clear cart

        return render_template(
            'thank_you_for_order.html',
            full_name=form_data['full_name'],
            email=form_data['email'],
            address=form_data['address'],
            payment_method=form_data['payment_method']
        )

    except sqlite3.Error as e:
        print("Error processing order:", e)
        flash("There was a problem placing your order.", "danger")
        return redirect(url_for('checkout'))


def get_user_id(first_name, last_name, cursor):
    """Fetches the user ID based on
     the first and last name."""
    cursor.execute('''SELECT id FROM users
     WHERE first_name = ? AND last_name = ?''',
                   (first_name, last_name))
    user_row = cursor.fetchone()
    return user_row[0] if user_row else None


def create_order(user_id, total, order_date, status, cursor):
    """Creates an order and
    returns the order ID."""
    cursor.execute('''INSERT INTO orders (user_id, total_price,
     order_date, status)
     VALUES (?, ?, ?, ?)''',
                   (user_id, total, order_date, status))
    return cursor.lastrowid


def add_items_to_order(cart_items, order_id, cursor):
    """Adds items from the cart to the order_items table."""
    for item in cart_items:
        cursor.execute('SELECT id FROM cookies WHERE name = ?',
                       (item['name'],))
        cookie_row = cursor.fetchone()
        if cookie_row:
            cookie_id = cookie_row[0]
            cursor.execute('''INSERT INTO order_items (order_id,
            cookie_id, quantity, price)
             VALUES (?, ?, ?, ?)''',
                           (order_id, cookie_id, item['quantity'],
                            item['price']))


@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    """Creates a new user account and stores it in the database."""
    try:
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone = request.form['phone']
        newsletter = request.form['newsletter']
        terms = request.form['terms']

        if password != confirm_password:
            return render_template(
                'signup.html',
                msg='Passwords do not match')

        if terms != 'on':
            return render_template(
                'signup.html',
                msg='Terms have not been accepted')

        with sqlite3.connect(app.config['DB_REF']) as conn:
            password_hash = hash_password(password)

            cursor = conn.cursor()
            cursor.execute('''
                        INSERT INTO users (
                            first_name,
                             last_name,
                              email,
                               password_hash,
                                phone_number,
                                 gets_newsletters
                        ) VALUES (?,?,?,?,?,?)''',
                           (first_name,
                            last_name,
                            email,
                            password_hash,
                            phone,
                            newsletter))
            conn.commit()
            target = 'thank_you.html'
            msg = ''
    except (KeyError, DatabaseError, ValueError) as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        target = 'signup.html'
        msg = 'Error: ' + str(e)
    return render_template(target, msg=msg)


@app.route('/signup')
def signup():
    """Displays the signup page."""
    return render_template('signup.html', msg='')

@app.route('/init', methods=['GET'])
def create_db():
    """Creates the SQLite database tables if they do not exist."""
    conn = sqlite3.connect(app.config['DB_REF'])
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            cookie_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (cookie_id) REFERENCES cookies (id)
        );
    ''')
    conn.commit()
    conn.close()

    # reset_cookies()
    seed_cookies()

# DANGER: this function will delete everything from the database.
# Use at your own risk.


def drop_db():
    """Drops all tables in the database (DANGEROUS)."""
    with sqlite3.connect((app.config['DB_REF'])) as conn:
        cursor = conn.cursor()

        cursor.execute('''DROP TABLE users''')
        conn.commit()
        cursor.execute('''DROP TABLE cookies''')
        conn.commit()
        cursor.execute('''DROP TABLE cart_items''')
        conn.commit()
        cursor.execute('''DROP TABLE orders''')
        conn.commit()


# DANGER: USE SPARINGLY!
# Make sure to clean up any lingering foreign keys before using this


def reset_cookies():
    """Deletes all entries from the cookies table."""
    try:
        with sqlite3.connect(app.config['DB_REF']) as conn:
            cursor = conn.cursor()

            cursor.execute('''DELETE FROM cookies''')
            conn.commit()
    except (sqlite3.DatabaseError, sqlite3.OperationalError)as e:
        conn.rollback()
        print("Failed to purge cookies table: " + str(e))
    finally:
        conn.close()


def read_csv():
    """Reads and returns contents of cookies_table.csv."""
    try:
        with open("cookies_table.csv", 'r', encoding='utf-8') as file_reader:
            reader = csv.reader(file_reader)
            output = list(reader)
    except (FileNotFoundError, IOError, csv.Error) as e:
        print("Error processing cookies_table.csv: " + str(e))
        output = []
    finally:
        file_reader.close()
    return output

def seed_cookies():
    """Seeds the cookies table from cookies_table.csv if empty."""
    try:
        with sqlite3.connect(app.config['DB_REF']) as conn:
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
                                            name, description,
                                             price,
                                              image_url,
                                               category
                                        ) VALUES (?,?,?,?,?); ''',
                                       [name, desc, price, img_url, cat])
                        conn.commit()
                    print("Cookies seeded")
                else:
                    print("No cookies to seed")
            else:
                print("Cookies already seeded")
    except (sqlite3.Error, ValueError, csv.Error) as e:
        conn.rollback()
        print("Error seeding cookies: " + str(e))
    finally:
        conn.close()

def seed_test_user():
    """Adds a test user to the users table."""
    with sqlite3.connect(app.config['DB_REF']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (
                first_name,
                 last_name,
                  email,
                   password_hash,
                    phone_number,
                     gets_newsletters
            ) VALUES (?,?,?,?,?,?); ''',
                       ['John',
                        'Doe',
                        'test@example.com',
                        hash_password('hashedpassword'),
                        '000-000-0000', 1])
        conn.commit()


@app.route('/logout')
def logout():
    """Logs the user out by clearing session data."""
    # Clear all session data
    session.clear()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for('home'))


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
