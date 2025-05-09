# Cookie Website

A delightful e-commerce website dedicated to selling artisanal, freshly-baked cookies. Our platform offers a seamless shopping experience for cookie enthusiasts to browse, order, and enjoy premium quality cookies delivered right to their doorstep.


![Build Status](https://img.shields.io/github/actions/workflow/status/Rhombu123/cookieWebsite/ci.yml?branch=main)

![Test Coverage](https://img.shields.io/badge/test%20coverage-100%25-brightgreen) 

##  Live Demo

🔗 **App**: [https://cookiewebsite.onrender.com](https://cookiewebsite.onrender.com)  
📦 **Repo**: [https://github.com/Rhombu123/cookieWebsite](https://github.com/Rhombu123/cookieWebsite)  
⚙️ **CI/CD Logs**: [GitHub Actions](https://github.com/Rhombu123/cookieWebsite/actions)  
📋 **Kanban Board**: [GitHub Projects](https://github.com/users/Rhombu123/projects/4/views/1)



## Features

- Browse and purchase delicious cookies
- User authentication and profile management
- Shopping cart functionality
- Order tracking and history
- Responsive design for all devices
- Newsletter subscription
- Wholesale and bulk order options

## User Profile Features

- View and update personal information (name, email, phone)
- Track order history with details (date, status, total)
- Manage newsletter preferences
- Secure authentication system

##  CI/CD Pipeline

CI/CD is handled with **GitHub Actions**:

- ✅ Linting using `pylint`
- ✅ Unit testing with `pytest`
- ✅ Deployment to **Render** on push to `main`
- ✅ Workflow halts if linting/tests fail

```yaml
Trigger: On push to main or PR
Jobs: Lint, Test, Deploy
Host: Render (via API)
```
 Stretch Goals Implemented

- ✅ CI/CD pipeline with linting, testing, and auto-deploy

- ✅ SSL via Render (automatic HTTPS)

- ✅ Persistent database using SQLite (extensible)

- ✅ Polished UI and bug-free UX

- ✅ Production-ready README

- ✅ GitHub Projects board for issue tracking

### Setup instructions (how to run it locally)

1. Clone the repository
       Open your terminal or command prompt and run the following command to clone the repository to your local machine:
        git clone (repository link), this will create a local copy of the repository.

2. Navigate to the project directory
        Once repository is cloned, navigate into the project using cd cookieWebsite

3. Set up a virtual environment (recommended)
        Create a virtual environment to manage the dependencies for the project.
        For macOS/Linux:
        python3 -m venv env
        source env/bin/activate
        
        For Windows:
        python -m venv env
        .\env\Scripts\activate

4. Install the required dependencies
       Now that the virtual environment is activated, install the necessary Python dependencies from the requirements.txt file by running the following command:
       pip install -r requirements.txt

5. Set up the database
       You need to set up the SQLite database for the project to work. To do this, run the following command to initialize the database:
       python app.py

6. Run the application
       Now that everything is set up, you can start the Flask development server. Run the following command:
        flask run
        The application will be available at http://127.0.0.1:5000

### How to use the App

1. Create an Account
   - Click on "Profile" in the navigation bar
   - Choose "Sign Up" and fill in your details
   - Complete the registration process

2. Browse Cookies
   - Visit the "Our Cookies" section to view all available cookies
   - Click on any cookie to view more details about it
   - View descriptions and prices for each cookie

3. Shopping
   - Add cookies to your shopping cart by selecting quantity
   - View your cart by clicking the shopping cart icon
   - Adjust quantities as needed
   - Proceed to checkout when ready

4. Profile Management
   - Access your profile through the navigation bar
   - Update your personal information
   - View your order history
   - Manage newsletter preferences

    
### Testing Instructions

- To run tests for the project using pytest, make sure the virtual environment is activated, and then run:
```yaml
pytest --cov=app test_app.py
pylint app.py
```

###  Deployment Instructions

1. Deploy to Render
Every time you push to the main branch, the CI/CD pipeline will automatically deploy your app. The steps for this are included in the GitHub Actions workflow. However, if you want to manually trigger a deploy, you can do so via the Render API by sending a POST request with the following command (configured in your GitHub Actions workflow):

```yaml
curl -X POST https://api.render.com/v1/services/srv-d0e1q4c9c44c73cgpfu0/deploys \
            -H "Authorization: Bearer ${{ secrets.project_scrt }}"
```

2. GitHub Actions for Deployment
The GitHub Actions workflow automatically triggers a deployment when code is pushed to the main branch. You can check the status of the build and deployment process in the GitHub Actions tab of your repository.
### Screenshots

Here are some screenshots of the working project:

![homepage-screenshot](images/homepagescreenshot.jpg)
*The homepage of the cookie website.*

![cookies](images/cookiesselection.jpg)
*Our cookies tab, displaying a list of available cookies.*

![cookie-view](images/vewcookie.jpg)
*Detailed view of a single cookie with options to add to the cart.*

![profile-view](images/profile-view.png)

![profile-edit-view](images/profile-edit-view.png)


### Security Features

- Secure password hashing using SHA-256
- Session management for user authentication
- CSRF protection for forms
- Input validation and sanitization
- Secure database operations with SQLite

### License

© 2024 Delicious Cookies. All Rights Reserved.
