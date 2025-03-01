from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
