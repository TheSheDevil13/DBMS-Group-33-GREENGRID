from flask import Flask, render_template
import pymysql

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
        # Test database connection by executing a simple query
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        return f"Connected to the database: {result[0]}"
    except Exception as e:
        return f"Error connecting to database: {e}"

# Route for Homepage (Static)
@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/login')
def login():
    return render_template('login.html')  

@app.route('/register')
def register():
    return render_template('register.html')  


if __name__ == '__main__':
    app.run(debug=True)
