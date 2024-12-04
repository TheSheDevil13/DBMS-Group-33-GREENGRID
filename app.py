from flask import Flask, render_template, request, redirect
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from templates.admin.admin_routes import admin_routes  # Import the admin routes

# Initialize the Flask app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True   # Add this line to disable template caching

# Connect to the MySQL database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',  # Leave empty if no password
    database='greengrid'
)

cursor = connection.cursor()

# Route to test database connection
@app.route('/test_db')
def test_db():
    try:
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        return f"Connected to the database: {result[0]}"
    except Exception as e:
        return f"Error connecting to database: {e}"

# Route for Homepage (Static)
@app.route('/')
def index():
    return render_template('index.html')

# Route for Login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for Login page (handles POST)
@app.route('/login-store', methods=['POST'])
def login_post():
    # Get data from the form
    email_username = request.form['email_username']
    password = request.form['password']
    
    # Initialize an error message variable
    error_message = None

    # Validation checks
    if not email_username or not password:
        error_message = "Email/Username and password are required."
    
    if error_message:
        return render_template('login.html', error=error_message)  # Pass error to template

    # Check user credentials (this is a simplified example)
    try:
        cursor.execute("SELECT PasswordHash FROM users WHERE Email = %s", (email,))
        result = cursor.fetchone()
        
        if result and check_password_hash(result[0], password):
            return redirect('/admin-dashboard')  # Redirect to dashboard on successful login
        else:
            error_message = "Invalid email or password."
    except Exception as e:
        error_message = f"Error: {e}"

    return render_template('login.html', error=error_message)  # Pass error to template

# Route for Register page (handles GET)
@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

# Route for Register page (handles POST)
@app.route('/register-store', methods=['POST'])
def register_post():
    # Get data from the form
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    
    # Initialize an error message variable
    error_message = None

    # Validation checks
    if not first_name or not last_name or not username or not email or not password or not role:
        error_message = "All fields are required."
    elif len(password) < 6:
        error_message = "Password must be at least 6 characters long."
    
    if error_message:
        return render_template('register.html', error=error_message)  # Pass error to template

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    status = 'pending'

    # Prepare the SQL query to insert user into the database
    query = """
    INSERT INTO users (FirstName, LastName, Username, Email, PasswordHash, Role, Status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        # Print the query and parameters for debugging
        print("Executing query:", query)
        print("With parameters:", (first_name, last_name, username, email, hashed_password, role, status))
        
        # Execute the query and commit the changes
        cursor.execute(query, (first_name, last_name, username, email, hashed_password, role, status))
        connection.commit()
        message = "Registration successful!"
        return redirect('/login')  # Redirect to the login page after successful registration
    except Exception as e:
        connection.rollback()  # Rollback in case of error
        print("Error during database operation:", e)  # Print the error for debugging
        error_message = f"Error: {e}"
    
    return render_template('register.html', error=error_message)  # Pass error to template

# Register the admin routes
app.register_blueprint(admin_routes)

if __name__ == '__main__':
    app.run(debug=True)
