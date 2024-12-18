from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, session
from werkzeug.security import generate_password_hash
import pymysql
import sys
from functools import wraps


admin_routes = Blueprint('admin', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Debug - Login Required: Checking authorization")
        print(f"Debug - Login Required: Session contents: {session}")
        print(f"Debug - Login Required: user_id in session: {'user_id' in session}")
        
        if 'user_id' not in session:
            print("Debug - Login Required: No user_id in session")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

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
            return redirect(url_for('admin.admin_agricultural_officers'))
        except Exception as e:
            conn.rollback()
            print("Error during database operation:", str(e))
            return redirect(url_for('admin.create_agricultural_officer'))
            
        finally:
            cursor.close()
            conn.close()

    return redirect("/admin/employee-directory/agricultural-officers")

@admin_routes.route('/admin/employee-directory/agricultural-officers/view/<int:id>')
@login_required
def view_agricultural_officer(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
            SELECT u.*, ud.ContactNumber, ud.Address 
            FROM users u 
            LEFT JOIN user_details ud ON u.UserID = ud.UserID 
            WHERE u.UserID = %s AND u.Role = 'O'
        """
        cursor.execute(query, (id,))
        officer = cursor.fetchone()
        if officer:
            # Convert None values to empty strings for better JSON handling
            for key in officer:
                if officer[key] is None:
                    officer[key] = ''
            return jsonify(officer)
        return jsonify({'error': 'Officer not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/agricultural-officers/edit/<int:id>', methods=['GET'])
@login_required
def edit_agricultural_officer(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        # Get officer details
        cursor.execute("""
            SELECT UserID, Username, FirstName, LastName, Email
            FROM users 
            WHERE UserID = %s AND Role = 'O'
        """, (id,))
        officer = cursor.fetchone()
        
        if not officer:
            flash('Officer not found', 'error')
            return redirect(url_for('admin.admin_agricultural_officers'))
            
        return render_template('admin/employee-directory/agricultural-officer/edit-agricultural-officer.html', officer=officer)
        
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('admin.admin_agricultural_officers'))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/agricultural-officers/edit/<int:id>', methods=['POST'])
@login_required
def edit_agricultural_officer_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validation
        if not firstname or not lastname or not username or not email:
            flash('All fields except password are required', 'error')
            return redirect(url_for('admin.edit_agricultural_officer', id=id))
            
        # Build update query
        if password and password.strip():
            # If password is provided, update it too
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute("""
                UPDATE users 
                SET FirstName = %s, LastName = %s, Username = %s, Email = %s, PasswordHash = %s
                WHERE UserID = %s AND Role = 'O'
            """, (firstname, lastname, username, email, hashed_password, id))
        else:
            # Don't update password if not provided
            cursor.execute("""
                UPDATE users 
                SET FirstName = %s, LastName = %s, Username = %s, Email = %s
                WHERE UserID = %s AND Role = 'O'
            """, (firstname, lastname, username, email, id))
            
        conn.commit()
        flash('Officer updated successfully', 'success')
        return redirect(url_for('admin.admin_agricultural_officers'))
        
    except Exception as e:
        conn.rollback()
        flash(str(e), 'error')
        return redirect(url_for('admin.edit_agricultural_officer', id=id))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/agricultural-officers/delete/<int:id>', methods=['POST'])
@login_required
def delete_agricultural_officer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First check if the officer exists
        cursor.execute("SELECT UserID FROM users WHERE UserID = %s AND Role = 'O'", (id,))
        if not cursor.fetchone():
            flash('Officer not found', 'error')
            return redirect(url_for('admin.admin_agricultural_officers'))
            
        # Delete the officer
        cursor.execute("DELETE FROM users WHERE UserID = %s AND Role = 'O'", (id,))
        conn.commit()
        flash('Officer deleted successfully', 'success')
        
    except Exception as e:
        conn.rollback()
        flash(str(e), 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('admin.admin_agricultural_officers'))

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


@admin_routes.route('/admin/employee-directory/agricultural-analysts/view/<int:id>')
@login_required
def view_agricultural_analyst(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
            SELECT u.*, ud.ContactNumber, ud.Address 
            FROM users u 
            LEFT JOIN user_details ud ON u.UserID = ud.UserID 
            WHERE u.UserID = %s AND u.Role = 'A'
        """
        cursor.execute(query, (id,))
        analyst = cursor.fetchone()
        if analyst:
            # Convert None values to empty strings for better JSON handling
            for key in analyst:
                if analyst[key] is None:
                    analyst[key] = ''
            return jsonify(analyst)
        return jsonify({'error': 'Analyst not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/agricultural-analysts/edit/<int:id>', methods=['GET'])
@login_required
def edit_agricultural_analyst(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        # Get analyst details
        cursor.execute("""
            SELECT UserID, Username, FirstName, LastName, Email
            FROM users 
            WHERE UserID = %s AND Role = 'A'
        """, (id,))
        analyst = cursor.fetchone()
        
        if not analyst:
            flash('Analyst not found', 'error')
            return redirect(url_for('admin.admin_agricultural_analysts'))
            
        return render_template('admin/employee-directory/agricultural-analyst/edit-agricultural-analyst.html', analyst=analyst)
        
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('admin.admin_agricultural_analysts'))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/agricultural-analysts/edit/<int:id>', methods=['POST'])
@login_required
def edit_agricultural_analyst_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validation
        if not firstname or not lastname or not username or not email:
            flash('All fields except password are required', 'error')
            return redirect(url_for('admin.edit_agricultural_analyst', id=id))
            
        # Build update query
        if password and password.strip():
            # If password is provided, update it too
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute("""
                UPDATE users 
                SET FirstName = %s, LastName = %s, Username = %s, Email = %s, PasswordHash = %s
                WHERE UserID = %s AND Role = 'A'
            """, (firstname, lastname, username, email, hashed_password, id))
        else:
            # Don't update password if not provided
            cursor.execute("""
                UPDATE users 
                SET FirstName = %s, LastName = %s, Username = %s, Email = %s
                WHERE UserID = %s AND Role = 'A'
            """, (firstname, lastname, username, email, id))
            
        conn.commit()
        flash('Analyst updated successfully', 'success')
        return redirect(url_for('admin.admin_agricultural_analysts'))
        
    except Exception as e:
        conn.rollback()
        flash(str(e), 'error')
        return redirect(url_for('admin.edit_agricultural_analyst', id=id))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/agricultural-analysts/delete/<int:id>', methods=['POST'])
@login_required
def delete_agricultural_analyst(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First check if the analyst exists
        cursor.execute("SELECT UserID FROM users WHERE UserID = %s AND Role = 'A'", (id,))
        if not cursor.fetchone():
            flash('Analyst not found', 'error')
            return redirect(url_for('admin.admin_agricultural_analysts'))
            
        # Delete the analyst
        cursor.execute("DELETE FROM users WHERE UserID = %s AND Role = 'A'", (id,))
        conn.commit()
        flash('Analyst deleted successfully', 'success')
        
    except Exception as e:
        conn.rollback()
        flash(str(e), 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('admin.admin_agricultural_analysts'))

@admin_routes.route('/admin/employee-directory/warehouse-managers')
def admin_warehouse_managers():
    # Create database connection
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to get results as dictionaries

    try:
        # Query to get all warehouse managers (users with Role 'W')
        query = "SELECT UserID, FirstName, LastName, Username, Email, Role FROM users WHERE Role = 'W'"
        cursor.execute(query)
        warehouse_managers = cursor.fetchall()
        
        return render_template('admin/employee-directory/warehouse-manager/warehouse-manager.html', warehouse_managers=warehouse_managers)
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('admin.admin_dashboard'))
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
            return redirect(url_for('admin.admin_warehouse_managers'))
        except Exception as e:
            conn.rollback()
            print("Error during database operation:", str(e))
            return redirect(url_for('admin.create_warehouse_manager'))
            
        finally:
            cursor.close()
            conn.close()

    return redirect("/admin/employee-directory/warehouse-managers")

@admin_routes.route('/admin/employee-directory/warehouse-managers/edit/<int:id>', methods=['GET'])
@login_required
def edit_warehouse_manager(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        # Get manager details
        cursor.execute("""
            SELECT UserID, Username, FirstName, LastName, Email
            FROM users 
            WHERE UserID = %s AND Role = 'W'
        """, (id,))
        manager = cursor.fetchone()
        
        if not manager:
            flash('Manager not found', 'error')
            return redirect(url_for('admin.admin_warehouse_managers'))
            
        return render_template('admin/employee-directory/warehouse-manager/edit-warehouse-manager.html', manager=manager)
        
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('admin.admin_warehouse_managers'))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/warehouse-managers/edit/<int:id>', methods=['POST'])
@login_required
def edit_warehouse_manager_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validation
        if not firstname or not lastname or not username or not email:
            flash('All fields except password are required', 'error')
            return redirect(url_for('admin.edit_warehouse_manager', id=id))
            
        # Build update query
        if password and password.strip():
            # If password is provided, update it too
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute("""
                UPDATE users 
                SET FirstName = %s, LastName = %s, Username = %s, Email = %s, PasswordHash = %s
                WHERE UserID = %s AND Role = 'W'
            """, (firstname, lastname, username, email, hashed_password, id))
        else:
            # Don't update password if not provided
            cursor.execute("""
                UPDATE users 
                SET FirstName = %s, LastName = %s, Username = %s, Email = %s
                WHERE UserID = %s AND Role = 'W'
            """, (firstname, lastname, username, email, id))
            
        conn.commit()
        flash('Manager updated successfully', 'success')
        return redirect(url_for('admin.admin_warehouse_managers'))
        
    except Exception as e:
        conn.rollback()
        flash(str(e), 'error')
        return redirect(url_for('admin.edit_warehouse_manager', id=id))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/employee-directory/warehouse-managers/delete/<int:id>', methods=['POST'])
@login_required
def delete_warehouse_manager(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First check if the manager exists
        cursor.execute("SELECT UserID FROM users WHERE UserID = %s AND Role = 'W'", (id,))
        if not cursor.fetchone():
            flash('Manager not found', 'error')
            return redirect(url_for('admin.admin_warehouse_managers'))
            
        # Delete the manager
        cursor.execute("DELETE FROM users WHERE UserID = %s AND Role = 'W'", (id,))
        conn.commit()
        flash('Manager deleted successfully', 'success')
        
    except Exception as e:
        conn.rollback()
        flash(str(e), 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('admin.admin_warehouse_managers'))

# Warehouse Management Routes
@admin_routes.route('/admin/warehouses')
@login_required
def list_warehouses():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT w.*, u.Username 
            FROM warehouse w 
            LEFT JOIN users u ON w.WEmployeeID = u.UserID
            ORDER BY w.WarehouseID
        """)
        warehouses = cursor.fetchall()
        return render_template('admin/warehouse-management/list.html', warehouses=warehouses)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect('/admin/admin-dashboard')
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/warehouses/create', methods=['GET', 'POST'])
@login_required
def create_warehouse():
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT UserID, Username FROM users WHERE Role = 'W'")
            employees = cursor.fetchall()
            return render_template('admin/warehouse-management/create.html', employees=employees)
        except Exception as e:
            flash(f"Error loading employees: {e}", "error")
            return redirect(url_for('admin.list_warehouses'))
        finally:
            cursor.close()
            conn.close()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get form data
        name = request.form['name'][:255]  # Limit to varchar(255)
        street = request.form['street']
        city = request.form['city']
        postal_code = request.form['postal_code']
        
        try:
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            light_exposure = float(request.form['light_exposure'])
        except ValueError:
            flash("Invalid numeric value for temperature, humidity, or light exposure", "error")
            return redirect(url_for('admin.create_warehouses'))
        
        employee_id = request.form['employee_id']
        
        # Validate data
        if not name or len(name.strip()) == 0:
            flash("Warehouse name is required", "error")
            return redirect(url_for('admin.create_warehouses'))
            
        if len(postal_code) != 6:
            flash("Postal code must be exactly 6 characters long", "error")
            return redirect(url_for('admin.create_warehouses'))
            
        # Validate decimal ranges
        if not (-999.99 <= temperature <= 999.99):
            flash("Temperature must be between -999.99 and 999.99", "error")
            return redirect(url_for('admin.create_warehouses'))
            
        if not (0 <= humidity <= 100):
            flash("Humidity must be between 0 and 100", "error")
            return redirect(url_for('admin.create_warehouses'))
            
        if not (0 <= light_exposure <= 9999.99):
            flash("Light exposure must be between 0 and 9999.99", "error")
            return redirect(url_for('admin.create_warehouses'))
        
        # Validate employee exists and has role 'W'
        cursor.execute("SELECT UserID FROM users WHERE UserID = %s AND Role = 'W'", (employee_id,))
        if not cursor.fetchone():
            flash("Invalid warehouse employee selected", "error")
            return redirect(url_for('admin.create_warehouses'))
        
        # Insert new warehouse
        cursor.execute("""
            INSERT INTO warehouse (Name, Street, City, PostalCode, Temperature, Humidity, LightExposure, WEmployeeID) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, street, city, postal_code, temperature, humidity, light_exposure, employee_id))
        conn.commit()
        flash("New warehouse added successfully!", "success")
        return redirect(url_for('admin.list_warehouses'))
    except Exception as e:
        conn.rollback()
        flash(f"Error adding warehouse: {e}", "error")
        return redirect(url_for('admin.create_warehouses'))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/warehouses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_warehouse(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        try:
            # Get warehouse data
            cursor.execute("SELECT * FROM warehouse WHERE WarehouseID = %s", (id,))
            warehouse = cursor.fetchone()
            
            # Get employees for dropdown
            cursor.execute("SELECT UserID, Username FROM users WHERE Role = 'W'")
            employees = cursor.fetchall()
            
            if warehouse:
                return render_template('admin/warehouse-management/edit.html', 
                                    warehouse=warehouse, employees=employees)
            flash("Warehouse not found!", "error")
            return redirect(url_for('admin.list_warehouses'))
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('admin.list_warehouses'))
        finally:
            cursor.close()
            conn.close()
    
    try:
        # Get form data
        name = request.form['name'][:255]  # Limit to varchar(255)
        street = request.form['street']
        city = request.form['city']
        postal_code = request.form['postal_code']
        
        try:
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            light_exposure = float(request.form['light_exposure'])
        except ValueError:
            flash("Invalid numeric value for temperature, humidity, or light exposure", "error")
            return redirect(url_for('admin.edit_warehouse', id=id))
        
        employee_id = request.form['employee_id']
        
        # Validate data
        if not name or len(name.strip()) == 0:
            flash("Warehouse name is required", "error")
            return redirect(url_for('admin.edit_warehouse', id=id))
            
        if len(postal_code) != 6:
            flash("Postal code must be exactly 6 characters long", "error")
            return redirect(url_for('admin.edit_warehouse', id=id))
            
        # Validate decimal ranges
        if not (-999.99 <= temperature <= 999.99):
            flash("Temperature must be between -999.99 and 999.99", "error")
            return redirect(url_for('admin.edit_warehouse', id=id))
            
        if not (0 <= humidity <= 100):
            flash("Humidity must be between 0 and 100", "error")
            return redirect(url_for('admin.edit_warehouse', id=id))
            
        if not (0 <= light_exposure <= 9999.99):
            flash("Light exposure must be between 0 and 9999.99", "error")
            return redirect(url_for('admin.edit_warehouse', id=id))
        
        # Validate employee exists and has role 'W'
        cursor.execute("SELECT UserID FROM users WHERE UserID = %s AND Role = 'W'", (employee_id,))
        if not cursor.fetchone():
            flash("Invalid warehouse employee selected", "error")
            return redirect(url_for('admin.edit_warehouse', id=id))
        
        # Update warehouse
        cursor.execute("""
            UPDATE warehouse 
            SET Name = %s, Street = %s, City = %s, PostalCode = %s, 
                Temperature = %s, Humidity = %s, LightExposure = %s,
                WEmployeeID = %s
            WHERE WarehouseID = %s
        """, (name, street, city, postal_code, temperature, humidity, light_exposure, employee_id, id))
        conn.commit()
        flash("Warehouse updated successfully!", "success")
        return redirect(url_for('admin.list_warehouses'))
    except Exception as e:
        conn.rollback()
        flash(f"Error updating warehouse: {e}", "error")
        return redirect(url_for('admin.edit_warehouse', id=id))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/warehouses/delete/<int:id>', methods=['POST'])
@login_required
def delete_warehouse(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM warehouse WHERE WarehouseID = %s", (id,))
        conn.commit()
        flash("Warehouse deleted successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting warehouse: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('admin.list_warehouses'))

# Shop Management Routes
@admin_routes.route('/admin/shop-management/shops')
@login_required
def list_shops():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT s.ShopID, s.ShopName, s.Street, s.Number, s.Email, 
                   s.PostalCode, s.City, 
                   u.Username as Owner,
                   CONCAT(s.Street, ', ', s.City) as Location
            FROM retailshop s 
            LEFT JOIN users u ON s.OwnerID = u.UserID
            ORDER BY s.ShopID DESC
        """)
        shops = cursor.fetchall()
        return render_template('admin/shop-management/shop/list.html', shops=shops)
    except Exception as e:
        print(f"Error in list_shops: {str(e)}")
        flash('An error occurred while fetching shops', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/shop-management/shops/create', methods=['GET', 'POST'])
@login_required
def create_shop():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        # Fetch shop owners for the dropdown
        cursor.execute("""
            SELECT UserID, Username 
            FROM users 
            WHERE Role = 'S' 
            ORDER BY Username
        """)
        shop_owners = cursor.fetchall()
        
        if request.method == 'POST':
            # Get form data
            shop_name = request.form.get('shop_name')
            street = request.form.get('street')
            number = request.form.get('number')
            email = request.form.get('email')
            postal_code = request.form.get('postal_code')
            city = request.form.get('city')
            owner_id = request.form.get('owner_id')
            
            # Insert new shop
            cursor.execute("""
                INSERT INTO retailshop (ShopName, Street, Number, Email, PostalCode, City, OwnerID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (shop_name, street, number, email, postal_code, city, owner_id))
            
            conn.commit()
            return redirect(url_for('admin.list_shops'))
            
        return render_template('admin/shop-management/shop/create.html', shop_owners=shop_owners)
        
    except Exception as e:
        if 'POST' in request.method:
            conn.rollback()
        print(f"Error in create_shop: {str(e)}")
        return redirect(url_for('admin.list_shops'))
        
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/shop-management/shop/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_shop(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        try:
            # Get shop details
            cursor.execute("""
                SELECT ShopID, ShopName, Street, Number, Email, 
                       PostalCode, City, OwnerID
                FROM retailshop
                WHERE ShopID = %s
            """, (id,))
            shop = cursor.fetchone()
            
            if not shop:
                flash('Shop not found.', 'error')
                return redirect(url_for('admin.list_shops'))
            
            # Get all shop owners for dropdown
            cursor.execute("""
                SELECT UserID, Username 
                FROM users 
                WHERE Role = 'S'
            """)
            shop_owners = cursor.fetchall()
            
            return render_template('admin/shop-management/shop/edit.html', 
                                 shop=shop, 
                                 shop_owners=shop_owners)
        except Exception as e:
            flash(f'Error loading shop: {str(e)}', 'error')
            return redirect(url_for('admin.list_shops'))
    
    try:
        # Get form data
        shop_name = request.form['shop_name']
        street = request.form['street']
        number = request.form['number']
        email = request.form['email']
        postal_code = request.form['postal_code']
        city = request.form['city']
        owner_id = request.form['owner_id']
        
        # Update shop
        cursor.execute("""
            UPDATE retailshop
            SET ShopName = %s, Street = %s, Number = %s, Email = %s,
                PostalCode = %s, City = %s, OwnerID = %s
            WHERE ShopID = %s
        """, (shop_name, street, number, email, postal_code, city, owner_id, id))
        
        conn.commit()
        flash('Shop updated successfully!', 'success')
        return redirect(url_for('admin.list_shops'))
    except Exception as e:
        conn.rollback()
        flash(f"Error updating shop: {str(e)}", "error")
        return redirect(url_for('admin.edit_shop', id=id))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/shops/delete/<int:id>', methods=['POST'])
@login_required
def delete_shop(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM retailshop WHERE ShopID = %s", (id,))
        conn.commit()
        return redirect(url_for('admin.list_shops'))
    except Exception as e:
        conn.rollback()
        print(f"Error deleting shop: {str(e)}")
        return redirect(url_for('admin.list_shops'))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/shop-management/shop-owners')
@login_required
def admin_shop_owners():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        cursor.execute("""
            SELECT u.UserID, u.FirstName, u.LastName, u.Username, u.Email,
                   COUNT(s.ShopID) as ShopCount
            FROM users u
            LEFT JOIN retailshop s ON u.UserID = s.OwnerID
            WHERE u.Role = 'S'
            GROUP BY u.UserID
        """)
        owners = cursor.fetchall()
        return render_template('admin/shop-management/owners/owners.html', owners=owners)
    except Exception as e:
        print(f"Error fetching shop owners: {str(e)}")
        flash('An error occurred while fetching shop owners', 'danger')
        return render_template('admin/shop-management/owners/owners.html', owners=[])
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/shop-management/shop-owners/create-owner', methods=['GET'])
def create_shop_owner():
    return render_template('admin/shop-management/owners/create-owner.html')

@admin_routes.route('/admin/shop-management/shop-owners/create-owner', methods=['POST'])
def create_shop_owner_post():
    if request.method == 'POST':
        # Get form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')  # Default is 123456
        role = 'S'  # Set role to 'S' for retail owners

        # Initialize error message
        error_message = None

        # Validation checks
        if not firstname or not lastname or not username or not email or not password:
            error_message = "All fields are required."
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters long."

        if error_message:
            return redirect(url_for('admin.create_shop_owner'))

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
            return redirect(url_for('admin.admin_shop_owners'))
        except Exception as e:
            conn.rollback()
            print("Error during database operation:", str(e))
            return redirect(url_for('admin.create_shop_owner'))
            
        finally:
            cursor.close()
            conn.close()

    return redirect("/admin/shop-management/shop-owners")

@admin_routes.route('/admin/shop-management/shop-owners/edit/<int:id>', methods=['GET'])
@login_required
def edit_shop_owner(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        # Get shop owner details
        cursor.execute("""
            SELECT UserID, Username, FirstName, LastName, Email
            FROM users 
            WHERE UserID = %s AND Role = 'S'
        """, (id,))
        owner = cursor.fetchone()
        
        if not owner:
            flash('Shop owner not found', 'error')
            return redirect(url_for('admin.admin_shop_owners'))
            
        return render_template('admin/shop-management/owners/edit-owner.html', owner=owner)
        
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('admin.admin_shop_owners'))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/shop-management/shop-owners/edit/<int:id>', methods=['POST'])
@login_required
def edit_shop_owner_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validation
        if not firstname or not lastname or not username or not email:
            flash('All fields except password are required', 'error')
            return redirect(url_for('admin.edit_shop_owner', id=id))
            
        # Build update query
        if password and password.strip():
            # If password is provided, update it too
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute("""
                UPDATE users 
                SET FirstName = %s, LastName = %s, Username = %s, Email = %s, PasswordHash = %s
                WHERE UserID = %s AND Role = 'S'
            """, (firstname, lastname, username, email, hashed_password, id))
        else:
            # Don't update password if not provided
            cursor.execute("""
                UPDATE users 
                SET FirstName = %s, LastName = %s, Username = %s, Email = %s
                WHERE UserID = %s AND Role = 'S'
            """, (firstname, lastname, username, email, id))
            
        conn.commit()
        flash('Shop owner updated successfully', 'success')
        return redirect(url_for('admin.admin_shop_owners'))
        
    except Exception as e:
        conn.rollback()
        flash(str(e), 'error')
        return redirect(url_for('admin.edit_shop_owner', id=id))
    finally:
        cursor.close()
        conn.close()

@admin_routes.route('/admin/shop-management/shop-owners/delete/<int:id>', methods=['POST'])
@login_required
def delete_shop_owner(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First delete all shops owned by this user
        cursor.execute("DELETE FROM retailshop WHERE OwnerID = %s", (id,))
        
        # Then delete the shop owner
        cursor.execute("DELETE FROM users WHERE UserID = %s AND Role = 'S'", (id,))
        conn.commit()
        
        return redirect(url_for('admin.admin_shop_owners'))
    except Exception as e:
        conn.rollback()
        print(f"Error in delete_shop_owner: {str(e)}")
        return redirect(url_for('admin.admin_shop_owners'))
    finally:
        cursor.close()
        conn.close()