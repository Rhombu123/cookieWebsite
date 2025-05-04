### App Description

The Cookie Website is an e-commerce platform dedicated to selling artisanal, freshly baked cookies. The platform offers users an easy way to browse a variety of cookies, add them to a shopping cart, and proceed with the checkout process to have them delivered to their doorstep. Users can view cookie details and explore various flavors and pricing.

### Feature List

#### Required Features (Must-have for minimum functionality)

    -Home: Displays an introduction to the Cookie Website and highlights featured cookies.
    -Our Cookies Page: Users can browse different cookie varieties available for purchase.
    -Shipping & Delivery Page: Displays details regarding shipping options, costs, and delivery times.
    -Wholesale & Bulk Orders Page: Offers information about bulk order discounts and options for businesses or large events.
    -Contact Us Page: Allows users to contact the website team for inquiries or support.
    -Login Page: Users can log in to their accounts to manage their orders or track their purchases.
    -Sign Up Page: Users can create a new account on the website.
    -Shopping Cart: Users can view their cart items, including the number of items and total quantity.

#### Should Have Features (Adds more value but not critical)

    -Search Bar: Users can search for specific cookies by name or ingredient.   
    -Responsive Design: Ensure that the website is optimized for mobile and tablet views.
    -User Reviews for Cookies: Allow customers to leave reviews or ratings for cookies.
    -Interactive Cookie Filtering: Filter cookies by categories like chocolate, nuts, or special diets (e.g., gluten-free).

#### Nice to Have Features (If there’s extra time)
    -Order History for Users: Allow users to view their past orders.
    -Admin Dashboard: A dashboard where an admin can manage cookies, process orders, and handle customer queries.
    -Email Notifications: Send automatic confirmation emails for orders, sign-ups, and more.
    -Password Recovery: Implement a password reset or recovery system for users.


### User Stories
    -As a customer, I want to browse the cookies available on the website so I can find the ones I want to purchase.
    -As a customer, I want to view detailed information about each cookie, such as the ingredients and price.
    -As a customer, I want to add cookies to my cart so I can later proceed to checkout.
    -As a customer, I want to learn about shipping costs and delivery times before making my purchase.
    -As a customer, I want to log in to my account to view or update my order information.
    -As an admin, I want to manage and update cookie products and information to ensure accurate data on the site.
    -As a customer, I want to contact the business if I have questions or need support.


### Database Schema (ERD) 

```mermaid


erDiagram
    USERS {
        int id PK
        string email
        string password_hash
        string name
        string address
    }
    COOKIES {
        int id PK
        string name
        string description
        decimal price
        string image_url
        string category
    }
    ORDERS {
        int id PK
        int user_id FK
        int cookie_id FK
        int quantity
        decimal total_price
        datetime order_date
        string status
    }
    CART_ITEMS {
        int id PK
        int user_id FK
        int cookie_id FK
        int quantity
    }
    
    USERS ||--o| ORDERS : places
    COOKIES ||--o| ORDERS : contains
    USERS ||--o| CART_ITEMS : has
    COOKIES ||--o| CART_ITEMS : includes
```

### User Flow Diagram
```mermaid
flowchart LR
    A[Home Page] --> B[Our Cookies]
    A --> C[Shipping & Delivery]
    A --> D[Wholesale & Bulk Orders]
    A --> E[Contact Us]
    A --> F[Login]
    A --> G[Sign Up]
    A --> H[Shopping Cart]
    
    F --> I[Login Page]
    G --> J[Sign Up Page]
    H --> K[Cart Details]
    B --> L[Cookie Details]
    B --> M[Add to Cart]
    L --> M
    K --> N[Checkout]
    N --> O[Payment]
    O --> P[Order Confirmation]

    I --> Q[Dashboard or Homepage after login]
    J --> Q
```

### List of Endpoints

### List of Endpoints – Routes (GET/POST) and Expected Input/Output

| Route                         | Method  | Input                                              | Output                                            |
|-------------------------------|---------|----------------------------------------------------|---------------------------------------------------|
| `/`                           | GET     | None                                               | Renders `index.html` (Home Page)                  |
| `/products`                   | GET     | None                                               | Renders `products.html` (List of Products)        |
| `/shipping`                   | GET     | None                                               | Renders `shipping.html` (Shipping info)           |
| `/wholesale`                  | GET     | None                                               | Renders `wholesale.html` (Wholesale info)         |
| `/contact`                    | GET     | None                                               | Renders `contact.html` (Contact Form)             |
| `/login`                      | GET     | None                                               | Renders `login.html` (Login Form)                 |
| `/cart`                       | GET     | None                                               | Renders `cart.html` (Shopping Cart)               |
| `/signup`                     | GET     | None                                               | Renders `signup.html` (Sign-Up Form)              |
| `/cart/add/<int:cookie_id>`   | POST    | `cookie_id`: ID of the cookie, `quantity`: Quantity of the cookie | Updates the cart and redirects to `/cart`          |
| `/cart/remove/<int:cookie_id>`| POST    | `cookie_id`: ID of the cookie to remove           | Updates the cart and redirects to `/cart`          |
| `/login`                      | POST    | `email`: User's email, `password`: User's password | Redirects to dashboard/home or shows error if invalid |
| `/signup`                     | POST    | `email`: User's email, `password`: User's password, `name`: User's full name, `address`: Shipping address | Redirects to login or home page, or shows error if invalid |
| `/checkout`                   | GET     | None                                               | Renders `checkout.html` (Checkout Page)           |
| `/payment`                    | POST    | Payment details (e.g., credit card information)    | Redirects to `order_confirmation.html` or shows payment error |
| `/order/confirmation`         | GET     | None                                               | Renders `order_confirmation.html` (Order Summary) |

### Update 1
#### New Feature
Jinja Template by Abdal, API code by Angel

- Users can now view their profile by going to /profile. There, they can view information about their account and orders.
- Users can now make changes to their account.

#### New Routes

| Route | Method | Input | Output |
| ----- | ------ | ----- |--------|
| `/profile` | GET | None | With `first_name` and `last_name` from session, renders `profile.html` (account info). Without session info, redirects to `/login`. |
| `/update_profile` | POST | `first_name`: User's first name, `last_name`: User's last name, `email`: User's email, `phone`: User's phone number, `newsletter`: whether the user wants to receive newsletters | Redirects to `/login` if user is not logged in, or to `/profile` after updating their info. |

### Tools used

#### Static Analysis - by Angel
**flake8**:
- Multiple lines: indentation, line too long, > or < blank lines.
- local variable 'full_name' is assigned to but never used
- local variable 'address' is assigned to but never used
- local variable 'payment_method' is assigned to but never used

**pylint**
- missing module docstrings
- missing function docstrings
- 'return' shadowed by the 'finally' clause. (return-in-finally)
- Catching too general exception Exception (broad-exception-caught)
- Redefining name 'cart' from outer scope (line 251) (redefined-outer-name)
- Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
- 'return' shadowed by the 'finally' clause. (return-in-finally)
- Catching too general exception Exception (broad-exception-caught)
- return statement in finally block may swallow exception (lost-exception)
- Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
- Catching too general exception Exception (broad-exception-caught)
- 'return' shadowed by the 'finally' clause. (return-in-finally)
- Catching too general exception Exception (broad-exception-caught)
- Using open without explicitly specifying an encoding (unspecified-encoding)
- return statement in finally block may swallow exception (lost-exception)
- Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
- Catching too general exception Exception (broad-exception-caught)
- standard import "sqlite3" should be placed before third party imports "flask.Flask", "flask.flash" (wrong-import-order)
- standard import "base64" should be placed before third party imports "flask.Flask", "flask.flash" (wrong-import-order)
- standard import "hashlib.sha256" should be placed before third party imports "flask.Flask", "flask.flash" (wrong-import-order)
- standard import "csv" should be placed before third party imports "flask.Flask", "flask.flash" (wrong-import-order)

#### Code Rating
- Rating before: 8.15/10
- Rating after: 10/10


#### Dynamic Analysis - by Anthony
**pytest**:
#### Test Coverage
Developed by Anthony

This app uses pytest for testing. Test configuration uses a separate sqlite file called `test_db.sqlite` which it seeds while building the test environment.
Tests cover signup/login functionality, profile accessing and updating, cart manipulation, and simply fetching the homepage. Login tests also test bad email/password inputs.
Most of the test cases focus on the status code of the response. 302 from `/login`, `/add_to_cart`, and `/clear_cart` indicate success. Some cases, like `/create_user`, return a new template depending on the outcome, so the test must instead check for key phrases in the response data.
The `/update_profile` test is unique among the other cases. In order to determine success, the test must follow the redirect and check the path.

### 