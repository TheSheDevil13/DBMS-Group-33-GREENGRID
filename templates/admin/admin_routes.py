from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash
import pymysql
import sys

admin_routes = Blueprint('admin', __name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  
        database='greengrid'
    )

@admin_routes.route('/admin/admin-dashboard')
def admin_dashboard():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT UserID, FirstName, LastName, Username, Email, Role, Status FROM users WHERE Status = 'pending'")
    pending_users = cursor.fetchall()
    # Convert tuple results to dictionaries for easier template access
    pending_users = [
        {
            'UserID': user[0],
            'FirstName': user[1],
            'LastName': user[2],
            'Username': user[3],
            'Email': user[4],
            'Role': user[5],
            'Status': user[6]
        }
        for user in pending_users
    ]
    return render_template('admin/admin-dashboard.html', pending_users=pending_users)

@admin_routes.route('/admin/approve-user/<int:user_id>', methods=['GET'])
def approve_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET Status = 'approved' WHERE UserID = %s", (user_id,))
    connection.commit()
    return redirect('/admin/admin-dashboard')

@admin_routes.route('/admin/reject-user/<int:user_id>', methods=['GET'])
def reject_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET Status = 'rejected' WHERE UserID = %s", (user_id,))
    connection.commit()
    return redirect('/admin/admin-dashboard')

@admin_routes.route('/admin/employee-directory/agricultural-officers', methods=['GET'])
def agricultural_officers():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT UserID, FirstName, LastName, Username, Email, Role, Status FROM users WHERE Status = 'pending' AND Role = 'O'")
    pending_users = cursor.fetchall()
    # Convert tuple results to dictionaries for easier template access
    pending_users = [
        {
            'UserID': user[0],
            'FirstName': user[1],
            'LastName': user[2],
            'Username': user[3],
            'Email': user[4],
            'Role': user[5],
            'Status': user[6]
        }
        for user in pending_users
    ]
    return render_template('admin/agricultural-officer.html', officers=pending_users)

@admin_routes.route('/admin/employee-directory/agricultural-officers/create', methods=['GET'])
def create_agricultural_officer():
    return render_template('admin/create-agricultural-officer.html')

@admin_routes.route('/admin/employee-directory/agricultural-officers/create-store', methods=['POST'])
def create_agricultural_officer_post():
    if request.method == 'POST':
        # Get form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')  # Default is 123456
        status = request.form.get('status')      # Default is pending
        role = 'O'

        # Initialize error message
        error_message = None

        # Validation checks
        if not firstname or not lastname or not username or not email or not password:
            error_message = "All fields are required."
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters long."

        if error_message:
            return redirect(url_for('admin.create_agricultural_officer'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Print query parameters for debugging
            query = """
            INSERT INTO users (FirstName, LastName, Username, Email, PasswordHash, Role, Status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (firstname, lastname, username, email, hashed_password, role, status)
            print("Executing query:", query)
            print("With parameters:", params)

            # Execute the query
            cursor.execute(query, params)
            conn.commit()
            return redirect(url_for('admin.agricultural_officers'))
        except Exception as e:
            conn.rollback()
            print("Error during database operation:", str(e))
            return redirect(url_for('admin.create_agricultural_officer'))
            
        finally:
            cursor.close()
            conn.close()

    return redirect("/admin/employee-directory/agricultural-officers")
