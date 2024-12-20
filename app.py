from flask import Flask, render_template, request, redirect, session, url_for, flash
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from templates.admin.admin_routes import admin_routes 
from templates.agricultural_officer.officer_routes import officer_routes 
from templates.farmer.farmer_routes import farmer_routes 
from templates.agricultural_analyst.analyst_route import analyst_routes
from templates.warehouse_manager.routes import warehouse_manager_routes
from templates.retail_shop.shop_routes import shop_routes

# Initialize the Flask app
app = Flask(__name__, template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Prevents Flask from caching static files
app.secret_key = 'your-secret-key-here'  # Add a secret key for session management

# Disable caching in development
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Connect to the MySQL database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',  # Leave empty if no password
    database='greengrid',
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

    # Check user credentials and get role
    try:
        cursor.execute("SELECT PasswordHash, Role FROM users WHERE Email = %s OR Username = %s", (email_username, email_username))
        result = cursor.fetchone()
        
        if result and check_password_hash(result[0], password):
            user_role = result[1].upper()  # Get user role and convert to uppercase
            print(f"Debug - User Role from DB: '{user_role}'")  # Debug print
            
            # Get full user details
            cursor.execute("""
                SELECT UserID, FirstName, LastName, Username, Email 
                FROM users 
                WHERE Email = %s OR Username = %s
            """, (email_username, email_username))
            user_details = cursor.fetchone()
            
            # Store user information in session
            session['user_id'] = user_details[0]
            session['username'] = user_details[3]
            session['email'] = user_details[4]
            session['role'] = user_role  # Store user role in session
            
            # Special check for admin (both username and email)
            if email_username.upper() == "ADMIN" or email_username == "admin@gmail.com":
                return redirect('/admin/admin-dashboard/'+email_username)

                
            
            # Redirect based on role for other users
            elif user_role == 'O':
                print("Debug - Matched officer role")  # Debug print
                return redirect('/agricultural-officer/officer-dashboard')
            elif user_role == 'W':
                print("Debug - Matched warehouse role")  # Debug print
                # Get warehouse manager's warehouse ID
                cursor.execute("""
                    SELECT WarehouseID 
                    FROM warehouse 
                    WHERE WEmployeeID = %s
                """, (user_details[0],))
                warehouse = cursor.fetchone()
                print(f"Debug - Login: Warehouse query result: {warehouse}")  # Debug print
                if warehouse:
                    session['warehouse_id'] = warehouse[0]
                    print(f"Debug - Login: Set warehouse_id in session to: {warehouse[0]}")  # Debug print
                else:
                    print("Debug - Login: No warehouse found for this manager")  # Debug print
                    flash('No warehouse assigned to this manager', 'error')
                    return redirect('/login')
                print(f"Debug - Login: Final session state: {session}")  # Debug print
                return redirect('/warehouse-manager/manager-dashboard')
            elif user_role == 'A':
                print("Debug - Matched analyst role")  # Debug print
                return redirect('/agricultural-analyst/analyst-dashboard')
            elif user_role == 'S':
                                # Get shop's ID
                cursor.execute("""
                    SELECT ShopID 
                    FROM retailshop 
                    WHERE OwnerID = %s
                """, (user_details[0],))
                shop = cursor.fetchone()
                print(f"Debug - Login: Shop query result: {shop}")  # Debug print
                if shop:
                    session['shop_id'] = shop[0]
                    print(f"Debug - Login: Set shop_id in session to: {shop[0]}")  # Debug print
                else:
                    print("Debug - Login: No shop found for this owner")  # Debug print
                    flash('No shop assigned to this owner', 'error')
                    return redirect('/login')
                return redirect('/shop/shop-dashboard')
            elif user_role == 'F':
                return redirect('/farmer/farmer-dashboard')
            else:
                print(f"Debug - No role match found for '{user_role}'")  # Debug print
                error_message = f"Invalid user role: '{user_role}'"
        else:
            error_message = "Invalid email/username or password."
    except Exception as e:
        error_message = f"Error: {e}"

    return render_template('login.html', error=error_message)

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
    INSERT INTO users (FirstName, LastName, Username, Email, PasswordHash, Role)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    try:
        # Print the query and parameters for debugging
        print("Executing query:", query)
        print("With parameters:", (first_name, last_name, username, email, hashed_password, role))
        
        # Execute the query and commit the changes
        cursor.execute(query, (first_name, last_name, username, email, hashed_password, role))
        connection.commit()
        return render_template('register.html', success="Registration successful! You can now log in.")
    except Exception as e:
        connection.rollback()  # Rollback in case of error
        print("Error during database operation:", e)  # Print the error for debugging
        error_message = f"Error: {e}"
    
    return render_template('register.html', error=error_message)  # Pass error to template


# Route for logout
@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    return redirect(url_for('login'))

# Register the admin routes
app.register_blueprint(admin_routes)
app.register_blueprint(officer_routes)
app.register_blueprint(farmer_routes)
app.register_blueprint(analyst_routes)
app.register_blueprint(warehouse_manager_routes)
app.register_blueprint(shop_routes)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=5000)
