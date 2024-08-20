# Flask-Based Web Application: README

## Project Overview

This project is a Flask-based web application designed to manage user registrations, logins, and content creation. The application connects to a MySQL database and uses several Flask extensions and Python libraries to implement various functionalities, including user authentication, session management, and form handling.

### Key Features

- **User Registration and Authentication:** Users can register, log in, and log out using secure password hashing with `passlib`.
- **Content Management:** Logged-in users can add, edit, delete, and view articles (referred to as "games" in the database).
- **Search Functionality:** Users can search for articles by keywords.
- **Form Validation:** The application uses `WTForms` for form handling and validation.
- **Session Management:** User sessions are managed using Flask's session mechanism to keep track of logged-in users.
- **Flash Messages:** Flash messages are used to provide feedback to the user, such as successful login, registration, or errors.

## Project Structure

### Main Python File (`app.py`)

The core of the application is in the `app.py` file, which contains:

- **Imports:**
  - Flask modules (`Flask`, `render_template`, `flash`, `redirect`, `url_for`, `session`, `logging`, `request`) to handle various web application tasks.
  - `MySQL` from `flask_mysqldb` to interact with the MySQL database.
  - `Form`, `StringField`, `TextAreaField`, `PasswordField`, and `validators` from `WTForms` for form handling and validation.
  - `sha256_crypt` from `passlib.hash` for secure password encryption.
  - `wraps` from `functools` to create custom decorators.

- **User Login Decorator:**
  - A custom `login_required` decorator is defined to restrict access to certain routes unless the user is logged in.

- **User Registration Form:**
  - A `RegisterForm` class is created using `WTForms` to validate user input during registration.

- **Sign In Form:**
  - A `LoginForm` class is created for user login validation.

- **Routes:**
  - `/` - Main page
  - `/about` - About Us page
  - `/dashboard` - Dashboard displaying user-specific articles (requires login)
  - `/article/<string:id>` - Display specific article details
  - `/articles` - Display all articles
  - `/register` - User registration page
  - `/login` - User login page
  - `/logout` - User logout (clears session)
  - `/delete/<string:id>` - Delete a specific article (requires login)
  - `/edit/<string:id>` - Edit a specific article (requires login)
  - `/addarticle` - Add a new article (requires login)
  - `/search` - Search for articles by keywords

### HTML Templates

The application uses several HTML templates located in the `templates/` directory. Each template is designed to serve a specific purpose:

- **`layout.html`**: The base template that includes the common layout for all pages.
- **`navbar.html`**: A reusable navigation bar included in various pages.
- **`formhelpers.html`**: Contains form helper macros used across the application.
- **`messages.html`**: Handles the display of flash messages.
- **`index.html`**: The main homepage of the application.
- **`about.html`**: An informational page about the application.
- **`register.html`**: A form page for user registration.
- **`login.html`**: A form page for user login.
- **`dashboard.html`**: The user's dashboard displaying their articles.
- **`article.html`**: Displays the details of a specific article.
- **`articles.html`**: Lists all available articles.
- **`addarticle.html`**: A form page for adding a new article.
- **`update.html`**: A form page for updating an existing article.

## Setup and Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Install dependencies:**

    Ensure you have Python and `pip` installed. Then install the required packages:

    ```bash
    pip install Flask Flask-MySQLdb WTForms passlib
    ```

3. **Set up the MySQL database:**

    Create a MySQL database and update the `app.py` file with your database credentials:

    ```python
    app.config["MYSQL_HOST"] = "localhost"
    app.config["MYSQL_USER"] = "your_mysql_user"
    app.config["MYSQL_PASSWORD"] = "your_mysql_password"
    app.config["MYSQL_DB"] = "your_database_name"
    ```

    Import the following SQL structure to your database:

    ```sql
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        username VARCHAR(50),
        email VARCHAR(100),
        password VARCHAR(100)
    );

    CREATE TABLE games (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100),
        author VARCHAR(50),
        content TEXT
    );
    ```

4. **Run the application:**

    Start the Flask application:

    ```bash
    python app.py
    ```

5. **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Contributing

If you would like to contribute to this project, please fork the repository, make your changes, and submit a pull request.
