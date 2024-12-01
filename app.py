from flask import Flask, render_template, request
import pymysql
from werkzeug.security import generate_password_hash

# Initialize the Flask app
app = Flask(__name__)

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

# Route for Register page (handles both GET and POST)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
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
        except Exception as e:
            connection.rollback()  # Rollback in case of error
            print("Error during database operation:", e)  # Print the error for debugging
            message = f"Error: {e}"
        
        return render_template('register.html', message=message)
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
