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
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # Get total products count
        cursor.execute("""
            SELECT COUNT(*) as total_count
            FROM product
        """)
        total_products = cursor.fetchone()['total_count']

        # Get pending orders count
        cursor.execute("""
            SELECT COUNT(*) as pending_count
            FROM `order` o
            WHERE o.OrderStatus = 'Pending'
        """)
        pending_count = cursor.fetchone()['pending_count']

        # Get recent orders with shop details
        cursor.execute("""
            SELECT o.OrderID, rs.ShopName, o.OrderStatus, DATE_FORMAT(o.OrderDate, '%Y-%m-%d') as OrderDate
            FROM `order` o
            JOIN retailshop rs ON o.ShopID = rs.ShopID
            WHERE o.OrderStatus IN ('Pending', 'Accepted', 'Delivered', 'Cancelled')
            ORDER BY o.OrderID DESC
            LIMIT 5
        """)
        recent_orders = cursor.fetchall()

        return render_template('agricultural_officer/dashboard/officer-dashboard.html', 
                             total_products=total_products,
                             pending_orders=pending_count,
                             recent_orders=recent_orders)
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "error")
        return redirect(url_for('login'))
    finally:
        cursor.close()
        conn.close()

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
            cursor.execute("""
                SELECT ProductID, ProductName, Category, PricePerUnit, Unit, Seasonality 
                FROM product 
                WHERE ProductID = %s AND OEmployeeID = %s
            """, (id, session['user_id']))
            product = cursor.fetchone()
            if product:
                print(f"Debug - Product from DB: {product}")  # Debug print
                return render_template('agricultural_officer/product/edit.html', product=product)
            flash("Product not found!", "error")
            return redirect('/agricultural-officer/products')
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect('/agricultural-officer/products')
        finally:
            cursor.close()
            conn.close()
    
    if request.method == 'POST':
        try:
            product_name = request.form['product_name']
            category = request.form['category']
            price_per_unit = request.form['price_per_unit']
            unit = request.form['unit']
            seasonality = request.form['seasonality']
            
            # Get current price before update
            cursor.execute("SELECT PricePerUnit FROM product WHERE ProductID = %s", (id,))
            current_price = cursor.fetchone()[0]
            
            # Only record price history if price has changed
            if str(current_price) != price_per_unit:
                cursor.execute("INSERT INTO price_history (ProductID, PricePerUnit) VALUES (%s, %s)",
                          (id, price_per_unit))
            
            cursor.execute("""
                UPDATE product 
                SET ProductName = %s, Category = %s, PricePerUnit = %s, Unit = %s, Seasonality = %s
                WHERE ProductID = %s AND OEmployeeID = %s
            """, (product_name, category, price_per_unit, unit, seasonality, id, session['user_id']))
            
            conn.commit()
            flash('Product updated successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error updating product: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect('/agricultural-officer/products')

@officer_routes.route('/agricultural-officer/products/delete/<int:id>')
@login_required
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Only delete if the product belongs to the logged-in officer
        cursor.execute("DELETE FROM product WHERE ProductID = %s AND OEmployeeID = %s", (id, session['user_id']))
        conn.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting product: {e}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect('/agricultural-officer/products')

# Product Management Routes Ends

# Order Management Routes
@officer_routes.route('/agricultural-officer/orders')
@login_required
def list_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get all orders with shop details
        cursor.execute("""
            SELECT o.OrderID, o.OrderDate, o.OrderStatus, 
                   s.ShopName, s.Street as ShopStreet, s.City as ShopCity,
                   COUNT(od.ProductID) as product_count,
                   w.Name as WarehouseName
            FROM `order` o
            JOIN retailshop s ON o.ShopID = s.ShopID
            LEFT JOIN warehouse w ON o.WarehouseID = w.WarehouseID
            LEFT JOIN order_details od ON o.OrderID = od.OrderID
            GROUP BY o.OrderID, o.OrderDate, o.OrderStatus, s.ShopName, s.Street, s.City, w.Name
            ORDER BY o.OrderDate DESC
        """)
        orders = cursor.fetchall()
        
        # Get all warehouses for assignment
        cursor.execute("SELECT WarehouseID, Name, City FROM warehouse")
        warehouses = cursor.fetchall()

        # Get demands for each shop
        cursor.execute("""
            SELECT 
                d.ShopID, 
                s.ShopName, 
                d.ProductID, 
                p.ProductName, 
                d.RequestedQuantity
            FROM 
                demand d
            JOIN 
                retailshop s ON d.ShopID = s.ShopID
            JOIN 
                product p ON d.ProductID = p.ProductID
        """)
        demands = cursor.fetchall()
        
        return render_template('agricultural_officer/orders/list.html', 
                             orders=orders, 
                             warehouses=warehouses,
                             product_requests=demands)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect(url_for('officer.officer_dashboard'))
    finally:
        cursor.close()
        conn.close()

@officer_routes.route('/agricultural-officer/orders/view/<int:id>')
@login_required
def view_order(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get order with shop details
        cursor.execute("""
            SELECT o.OrderID, o.OrderDate, o.OrderStatus, 
                   s.ShopName, s.Street as ShopStreet, s.City as ShopCity,
                   o.WarehouseID, w.Name as WarehouseName
            FROM `order` o
            JOIN retailshop s ON o.ShopID = s.ShopID
            LEFT JOIN warehouse w ON o.WarehouseID = w.WarehouseID
            WHERE o.OrderID = %s
        """, (id,))
        order = cursor.fetchone()
        
        if not order:
            flash("Order not found", "error")
            return redirect(url_for('officer.list_orders'))

        # Get product details
        cursor.execute("""
            SELECT p.ProductName, od.OrderQuantity, p.Unit
            FROM order_details od
            JOIN product p ON od.ProductID = p.ProductID
            WHERE od.OrderID = %s
        """, (id,))
        products = cursor.fetchall()
        
        # Get warehouses for assignment
        cursor.execute("SELECT WarehouseID, Name, City FROM warehouse")
        warehouses = cursor.fetchall()
        
        return render_template('agricultural_officer/orders/details.html', 
                             order=order, products=products, warehouses=warehouses)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect(url_for('officer.list_orders'))
    finally:
        cursor.close()
        conn.close()

@officer_routes.route('/agricultural-officer/orders/process', methods=['POST'])
@login_required
def process_order():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        order_id = request.form.get('order_id')
        warehouse_id = request.form.get('warehouse_id')
        action = request.form.get('action')
        
        if not order_id or not warehouse_id or not action:
            flash("Missing required parameters", "error")
            return redirect(url_for('officer.list_orders'))
            
        if action == 'accept':
            # Update order status and assign warehouse
            cursor.execute("""
                UPDATE `order` 
                SET OrderStatus = 'Accepted', WarehouseID = %s
                WHERE OrderID = %s AND OrderStatus = 'Pending'
            """, (warehouse_id, order_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                flash("Order accepted and assigned to warehouse successfully", "success")
            else:
                flash("Order could not be processed", "error")
        else:
            flash("Invalid action", "error")
            
        return redirect(url_for('officer.list_orders'))
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "error")
        return redirect(url_for('officer.list_orders'))
    finally:
        cursor.close()
        conn.close()