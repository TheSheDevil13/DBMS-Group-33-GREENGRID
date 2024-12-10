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
    return render_template('admin/dashboard/admin-dashboard.html')

@admin_routes.route('/admin/employee-directory/agricultural-officers')
def admin_agricultural_officers():
    # Create database connection
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to get results as dictionaries

    try:
        # Query to get all agricultural officers (users with Role 'O')
        query = "SELECT UserID, FirstName, LastName, Username, Email, Role FROM users WHERE Role = 'O'"
        cursor.execute(query)
        officers = cursor.fetchall()
        
        return render_template('admin/employee-directory/agricultural-officer/agricultural-officer.html', officers=officers)
    except Exception as e:
        print("Error fetching agricultural officers:", str(e))
        return render_template('admin/employee-directory/agricultural-officer/agricultural-officer.html', officers=[])
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/agricultural-officers/create', methods=['GET'])
def create_agricultural_officer():
    return render_template('admin/employee-directory/agricultural-officer/create-agricultural-officer.html')

@admin_routes.route('/admin/employee-directory/agricultural-officers/create-store', methods=['POST'])
def create_agricultural_officer_post():
    if request.method == 'POST':
        # Get form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')  # Default is 123456
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
            INSERT INTO users (FirstName, LastName, Username, Email, PasswordHash, Role)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (firstname, lastname, username, email, hashed_password, role)
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


@admin_routes.route('/admin/employee-directory/agricultural-analysts')
def admin_agricultural_analysts():
    # Create database connection
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to get results as dictionaries

    try:
        # Query to get all agricultural officers (users with Role 'O')
        query = "SELECT UserID, FirstName, LastName, Username, Email, Role FROM users WHERE Role = 'A'"
        cursor.execute(query)
        analysts = cursor.fetchall()
        
        return render_template('admin/employee-directory/agricultural-analyst/agricultural-analyst.html', analysts=analysts)
    except Exception as e:
        print("Error fetching agricultural officers:", str(e))
        return render_template('admin/employee-directory/agricultural-analyst/agricultural-analyst.html', analysts=[])
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/agricultural-analysts/create', methods=['GET'])
def create_agricultural_analyst():
    return render_template('admin/employee-directory/agricultural-analyst/create-agricultural-analyst.html')

@admin_routes.route('/admin/employee-directory/agricultural-analysts/create-store', methods=['POST'])
def create_agricultural_analyst_post():
    if request.method == 'POST':
        # Get form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')  # Default is 123456
        role = 'A'

        # Initialize error message
        error_message = None

        # Validation checks
        if not firstname or not lastname or not username or not email or not password:
            error_message = "All fields are required."
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters long."

        if error_message:
            return redirect(url_for('admin.create_agricultural_analyst'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Print query parameters for debugging
            query = """
            INSERT INTO users (FirstName, LastName, Username, Email, PasswordHash, Role)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (firstname, lastname, username, email, hashed_password, role)
            print("Executing query:", query)
            print("With parameters:", params)

            # Execute the query
            cursor.execute(query, params)
            conn.commit()
            return redirect(url_for('admin.admin_agricultural_analysts'))
        except Exception as e:
            conn.rollback()
            print("Error during database operation:", str(e))
            return redirect(url_for('admin.create_agricultural_analyst'))
            
        finally:
            cursor.close()
            conn.close()

    return redirect("/admin/employee-directory/agricultural-analysts")


@admin_routes.route('/admin/employee-directory/warehouse-managers')
def admin_warehouse_managers():
    # Create database connection
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to get results as dictionaries

    try:
        # Query to get all agricultural officers (users with Role 'O')
        query = "SELECT UserID, FirstName, LastName, Username, Email, Role FROM users WHERE Role = 'W'"
        cursor.execute(query)
        managers = cursor.fetchall()
        
        return render_template('admin/employee-directory/warehouse-manager/warehouse-manager.html', managers=managers)
    except Exception as e:
        print("Error fetching agricultural officers:", str(e))
        return render_template('admin/employee-directory/warehouse-manager/warehouse-manager.html', managers=[])
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/warehouse-managers/create', methods=['GET'])
def create_warehouse_manager():
    return render_template('admin/employee-directory/warehouse-manager/create-warehouse-manager.html')

@admin_routes.route('/admin/employee-directory/warehouse-managers/create-store', methods=['POST'])
def create_warehouse_manager_post():
    if request.method == 'POST':
        # Get form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')  # Default is 123456
        role = 'W'

        # Initialize error message
        error_message = None

        # Validation checks
        if not firstname or not lastname or not username or not email or not password:
            error_message = "All fields are required."
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters long."

        if error_message:
            return redirect(url_for('admin.create_warehouse_manager'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Print query parameters for debugging
            query = """
            INSERT INTO users (FirstName, LastName, Username, Email, PasswordHash, Role)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (firstname, lastname, username, email, hashed_password, role)
            print("Executing query:", query)
            print("With parameters:", params)

            # Execute the query
            cursor.execute(query, params)
            conn.commit()
            return redirect(url_for('admin.warehouse_managers'))
        except Exception as e:
            conn.rollback()
            print("Error during database operation:", str(e))
            return redirect(url_for('admin.create_warehouse_manager'))
            
        finally:
            cursor.close()
            conn.close()

    return redirect("/admin/employee-directory/warehouse-managers")
