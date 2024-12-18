from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, session
from werkzeug.security import generate_password_hash
import pymysql
import sys
from functools import wraps


officer_routes = Blueprint('officer', __name__)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"Debug: Checking login - user_id: {session.get('user_id')}, role: {session.get('role')}")
        if 'user_id' not in session or session.get('role') != 'O':
            print("Debug: Login check failed - redirecting to login")
            return redirect('/login')
        print("Debug: Login check passed")
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  
        database='greengrid'
    )

@officer_routes.route('/agricultural-officer/officer-dashboard')
@login_required
def officer_dashboard():
    return render_template('agricultural_officer/dashboard/officer-dashboard.html')

# Product Management Routes Starts
@officer_routes.route('/agricultural-officer/products')
@login_required
def list_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get only products created by the logged-in officer
    cursor.execute("""
        SELECT ProductID, ProductName, Category, PricePerUnit, Unit, Seasonality 
        FROM product 
        WHERE OEmployeeID = %s
        ORDER BY ProductID DESC
    """, (session['user_id'],))
    
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('agricultural_officer/product/list.html', products=products)

@officer_routes.route('/agricultural-officer/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'GET':
        return render_template('agricultural_officer/product/create.html')
    
    if request.method == 'POST':
        product_name = request.form['product_name']
        category = request.form['category']
        price_per_unit = request.form['price_per_unit']
        unit = request.form['unit']
        seasonality = request.form['seasonality']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert product with the officer's ID
        cursor.execute("""
            INSERT INTO product (ProductName, Category, PricePerUnit, Unit, Seasonality, OEmployeeID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (product_name, category, price_per_unit, unit, seasonality, session['user_id']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Product created successfully!', 'success')
        return redirect(url_for('officer.list_products'))

@officer_routes.route('/agricultural-officer/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM product WHERE ProductID = %s", (id,))
            product = cursor.fetchone()
            if product:
                return render_template('agricultural_officer/product/edit.html', product=product)
            flash("Product not found!", "error")
            return redirect('/agricultural-officer/products')
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect('/agricultural-officer/products')
        finally:
            cursor.close()
            conn.close()
    
    try:
        # Get form data
        product_name = request.form['product_name']
        category = request.form['category']
        price_per_unit = request.form['price_per_unit']
        unit = request.form['unit']
        seasonality = request.form['seasonality']
        
        # Update product
        cursor.execute("""
            UPDATE product 
            SET ProductName = %s, Category = %s, PricePerUnit = %s, Unit = %s, Seasonality = %s
            WHERE ProductID = %s
        """, (product_name, category, price_per_unit, unit, seasonality, id))
        conn.commit()
        flash("Product updated successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error updating product: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect('/agricultural-officer/products')

@officer_routes.route('/agricultural-officer/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM product WHERE ProductID = %s", (id,))
        conn.commit()
        flash("Product deleted successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting product: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect('/agricultural-officer/products')
# Product Management Routes Ends