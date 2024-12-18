from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, session
from functools import wraps
import pymysql
import sys
from datetime import datetime

shop_routes = Blueprint('shop', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        if session.get('role') != 'S':
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

@shop_routes.route('/shop/shop-dashboard')
@login_required
def shop_dashboard():
    try:
        return render_template('retail_shop/dashboard/dashboard.html')
    except Exception as e:
        print(f"Error rendering dashboard: {str(e)}")
        raise

# Order Management Routes
@shop_routes.route('/shop/orders')
@login_required
def list_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT o.OrderID, o.OrderDate, o.OrderStatus, o.ShopID, s.ShopName,
                   COUNT(od.ProductID) as product_count
            FROM `order` o
            JOIN retailshop s ON o.ShopID = s.ShopID
            LEFT JOIN order_details od ON o.OrderID = od.OrderID
            WHERE o.ShopID = %s
            GROUP BY o.OrderID, o.OrderDate, o.OrderStatus, o.ShopID, s.ShopName
            ORDER BY o.OrderID DESC
        """, (session['shop_id'],))
        orders = list(cursor.fetchall())

        # Get product details for each order
        for i, order in enumerate(orders):
            cursor.execute("""
                SELECT od.OrderID, od.ProductID, od.OrderQuantity, p.Unit, p.ProductName
                FROM order_details od
                JOIN product p ON od.ProductID = p.ProductID
                WHERE od.OrderID = %s
            """, (order[0],))
            orders[i] = order + (cursor.fetchall(),)

        return render_template('retail_shop/order/list.html', orders=orders)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect('/shop/shop-dashboard')
    finally:
        cursor.close()
        conn.close()

@shop_routes.route('/shop/orders/create', methods=['GET', 'POST'])
@login_required
def create_order():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        try:
            # Get products
            cursor.execute("SELECT ProductID, ProductName, Unit, PricePerUnit FROM product ORDER BY ProductName")
            products = cursor.fetchall()
            
            return render_template('retail_shop/order/create.html', products=products)
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('shop.list_orders'))
        finally:
            cursor.close()
            conn.close()
    
    try:
        # Validate input data
        shop_id = session.get('shop_id')
        if not shop_id:
            flash("Shop ID not found in session", "error")
            return redirect(url_for('shop.list_orders'))
            
        products = request.form.getlist('products[]')
        quantities = request.form.getlist('quantities[]')
        
        # Validate products and quantities
        if len(products) != len(quantities):
            flash("Invalid product data submitted", "error")
            return redirect(url_for('shop.create_order'))
            
        if not products or not quantities:
            flash("Please add at least one product", "error")
            return redirect(url_for('shop.create_order'))
            
        # Validate quantities are positive numbers
        for qty in quantities:
            try:
                if float(qty) <= 0:
                    flash("Quantities must be positive numbers", "error")
                    return redirect(url_for('shop.create_order'))
            except ValueError:
                flash("Invalid quantity value", "error")
                return redirect(url_for('shop.create_order'))

        # Insert main order
        cursor.execute("""
            INSERT INTO `order` (OrderDate, OrderStatus, ShopID)
            VALUES (CURDATE(), 'Pending', %s)
        """, (shop_id,))
        
        order_id = cursor.lastrowid

        # Insert order details
        for product_id, quantity in zip(products, quantities):
            # Verify product exists
            cursor.execute("SELECT ProductID FROM product WHERE ProductID = %s", (product_id,))
            if not cursor.fetchone():
                conn.rollback()
                flash(f"Invalid product ID: {product_id}", "error")
                return redirect(url_for('shop.create_order'))
                
            cursor.execute("""
                INSERT INTO order_details (OrderID, ProductID, OrderQuantity)
                VALUES (%s, %s, %s)
            """, (order_id, product_id, quantity))

        conn.commit()
        flash("Order created successfully!", "success")
        return redirect(url_for('shop.list_orders'))
    except Exception as e:
        conn.rollback()
        flash(f"Error creating order: {e}", "error")
        return redirect(url_for('shop.create_order'))
    finally:
        cursor.close()
        conn.close()

@shop_routes.route('/shop/get-product-unit/<int:product_id>')
@login_required
def get_product_unit(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Unit FROM product WHERE ProductID = %s", (product_id,))
        result = cursor.fetchone()
        if result:
            return jsonify({'unit': result[0]})
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@shop_routes.route('/shop/orders/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        try:
            # Verify order belongs to current shop
            cursor.execute("""
                SELECT o.OrderID, o.OrderDate, o.OrderStatus, o.ShopID, s.ShopName,
                       COUNT(od.ProductID) as product_count, o.WarehouseID
                FROM `order` o
                JOIN retailshop s ON o.ShopID = s.ShopID
                LEFT JOIN order_details od ON o.OrderID = od.OrderID
                WHERE o.OrderID = %s AND o.ShopID = %s
                GROUP BY o.OrderID, o.OrderDate, o.OrderStatus, o.ShopID, s.ShopName, o.WarehouseID
            """, (id, session.get('shop_id')))
            order = cursor.fetchone()
            
            if not order:
                flash("Order not found or access denied", "error")
                return redirect('/shop/orders')

            # Get product details with unit from product table
            cursor.execute("""
                SELECT od.OrderID, od.ProductID, od.OrderQuantity, p.Unit, p.ProductName, p.PricePerUnit
                FROM order_details od
                JOIN product p ON od.ProductID = p.ProductID
                WHERE od.OrderID = %s
            """, (id,))
            products = cursor.fetchall()

            # Get all products for dropdown
            cursor.execute("SELECT ProductID, ProductName, Unit, PricePerUnit FROM product")
            all_products = cursor.fetchall()

            return render_template('retail_shop/order/edit.html', 
                                 order=order, 
                                 order_products=products,
                                 all_products=all_products)

        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect('/shop/orders')
        finally:
            cursor.close()
            conn.close()

    elif request.method == 'POST':
        try:
            # Verify order belongs to current shop and can be edited
            cursor.execute("""
                SELECT OrderStatus FROM `order` 
                WHERE OrderID = %s AND ShopID = %s
            """, (id, session.get('shop_id')))
            current_order = cursor.fetchone()
            
            if not current_order:
                flash("Order not found or access denied", "error")
                return redirect('/shop/orders')
                
            if current_order[0] not in ['Pending', 'Cancelled']:
                flash("Cannot edit order in current status", "error")
                return redirect('/shop/orders')

            status = request.form.get('status', 'Pending')
            product_ids = request.form.getlist('product_id[]')
            quantities = request.form.getlist('quantity[]')
            
            # Validate input
            if len(product_ids) != len(quantities):
                flash("Invalid product data submitted", "error")
                return redirect(url_for('shop.edit_order', id=id))
                
            if not product_ids or not quantities:
                flash("Please add at least one product", "error")
                return redirect(url_for('shop.edit_order', id=id))
            
            # Start transaction
            conn.begin()
            
            # Update order status
            cursor.execute("""
                UPDATE `order` 
                SET OrderStatus = %s
                WHERE OrderID = %s AND ShopID = %s
            """, (status, id, session.get('shop_id')))

            # Delete existing order details
            cursor.execute("DELETE FROM order_details WHERE OrderID = %s", (id,))

            # Insert new order details
            for product_id, quantity in zip(product_ids, quantities):
                try:
                    qty = float(quantity)
                    if qty <= 0:
                        raise ValueError("Quantity must be positive")
                except ValueError:
                    conn.rollback()
                    flash("Invalid quantity value", "error")
                    return redirect(url_for('shop.edit_order', id=id))
                    
                # Verify product exists
                cursor.execute("SELECT ProductID FROM product WHERE ProductID = %s", (product_id,))
                if not cursor.fetchone():
                    conn.rollback()
                    flash(f"Invalid product ID: {product_id}", "error")
                    return redirect(url_for('shop.edit_order', id=id))
                
                cursor.execute("""
                    INSERT INTO order_details (OrderID, ProductID, OrderQuantity)
                    VALUES (%s, %s, %s)
                """, (id, product_id, quantity))

            conn.commit()
            flash("Order updated successfully", "success")
            return redirect(url_for('shop.list_orders'))

        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "error")
            return redirect(url_for('shop.edit_order', id=id))
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('shop.list_orders'))

@shop_routes.route('/shop/orders/delete/<int:id>', methods=['POST'])
@login_required
def delete_order(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        print(f"Attempting to delete order {id}")  # Debug log
        
        # First verify the order belongs to the current shop
        cursor.execute("SELECT ShopID, OrderStatus FROM `order` WHERE OrderID = %s", (id,))
        order = cursor.fetchone()
        print(f"Order details: {order}")  # Debug log
        
        if not order or order[0] != session.get('shop_id'):
            print(f"Access denied. Shop ID: {session.get('shop_id')}")  # Debug log
            flash("Order not found or access denied", "error")
            return redirect(url_for('shop.list_orders'))

        # Start transaction
        cursor.execute("START TRANSACTION")
        print("Transaction started")  # Debug log

        # Delete from all related tables in correct order
        print("Deleting from dispatch...")  # Debug log
        cursor.execute("DELETE FROM dispatch WHERE OrderID = %s", (id,))
        print(f"Dispatch rows affected: {cursor.rowcount}")  # Debug log
        
        print("Deleting from order_details...")  # Debug log
        cursor.execute("DELETE FROM order_details WHERE OrderID = %s", (id,))
        print(f"Order details rows affected: {cursor.rowcount}")  # Debug log
        
        print("Deleting from order...")  # Debug log
        cursor.execute("DELETE FROM `order` WHERE OrderID = %s", (id,))
        print(f"Order rows affected: {cursor.rowcount}")  # Debug log
        
        # Commit transaction
        conn.commit()
        print("Transaction committed")  # Debug log
        flash("Order deleted successfully!", "success")
    except Exception as e:
        # Rollback transaction on error
        conn.rollback()
        print(f"Error in delete_order: {str(e)}")  # Debug log
        print(f"Full error details: {type(e).__name__}: {str(e)}")  # More detailed error log
        flash(f"Error deleting order: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('shop.list_orders'))

@shop_routes.route('/shop/orders/view/<int:id>')
@login_required
def view_order(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get order with shop and warehouse details
        cursor.execute("""
            SELECT o.OrderID, o.OrderDate as OrderDate, 
                   o.OrderStatus, o.ShopID, s.ShopName, o.WarehouseID,
                   w.Name as WarehouseName, w.Street as WarehouseStreet,
                   w.City as WarehouseCity
            FROM `order` o
            JOIN retailshop s ON o.ShopID = s.ShopID
            LEFT JOIN warehouse w ON o.WarehouseID = w.WarehouseID
            WHERE o.OrderID = %s
        """, (id,))
        order = cursor.fetchone()
        
        if not order:
            flash("Order not found", "error")
            return redirect('/shop/orders')

        # Get product details
        cursor.execute("""
            SELECT p.ProductName, od.OrderQuantity, p.Unit
            FROM order_details od
            JOIN product p ON od.ProductID = p.ProductID
            WHERE od.OrderID = %s
        """, (id,))
        products = cursor.fetchall()
        
        # Add products to the order tuple
        order = order + (products,)

        return render_template('retail_shop/order/details.html', order=order)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect('/shop/orders')
    finally:
        cursor.close()
        conn.close()

@shop_routes.route('/shop/get-order-details')
@login_required
def get_order_details():
    order_id = request.args.get('order_id')
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT 
                od.ProductID,
                od.OrderID,
                p.ProductName as product_name,
                od.OrderQuantity as ordered_quantity,
                p.Unit as unit,
                SUM(CASE 
                    WHEN s.StockAvailability = 'Incoming' THEN s.StockQuantity 
                    WHEN s.StockAvailability = 'Outgoing' THEN -s.StockQuantity 
                    ELSE 0 
                END) as available_quantity
            FROM order_details od
            JOIN product p ON od.ProductID = p.ProductID
            JOIN `order` o ON od.OrderID = o.OrderID
            LEFT JOIN stock s ON od.ProductID = s.ProductID AND o.WarehouseID = s.WarehouseID
            WHERE od.OrderID = %s
            GROUP BY od.ProductID, p.ProductName, p.Unit
        """, (order_id,))
        products = cursor.fetchall()
        return jsonify({'products': products})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
