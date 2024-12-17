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
            cursor.execute("SELECT ProductID, ProductName FROM product ORDER BY ProductName")
            products = cursor.fetchall()
            
            # Get shops
            cursor.execute("SELECT ShopID, ShopName FROM retailshop ORDER BY ShopName")
            shops = cursor.fetchall()
            
            return render_template('retail_shop/order/create.html', 
                                products=products, shops=shops)
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('shop.list_orders'))
        finally:
            cursor.close()
            conn.close()
    
    try:
        # Get form data
        shop_id = session['shop_id']  # Get shop_id from session
        order_status = request.form['order_status']
        products = request.form.getlist('products[]')
        quantities = request.form.getlist('quantities[]')

        # Insert main order
        cursor.execute("""
            INSERT INTO `order` (OrderDate, OrderStatus, ShopID)
            VALUES (CURDATE(), %s, %s)
        """, (order_status, shop_id))
        
        order_id = cursor.lastrowid

        # Insert order details
        for i in range(len(products)):
            cursor.execute("""
                INSERT INTO order_details (OrderID, ProductID, OrderQuantity)
                VALUES (%s, %s, %s)
            """, (order_id, products[i], quantities[i]))

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

@shop_routes.route('/shop/orders/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        try:
            # Get order with shop details
            cursor.execute("""
                SELECT o.OrderID, o.OrderDate, o.OrderStatus, o.ShopID, s.ShopName,
                       COUNT(od.ProductID) as product_count, o.WarehouseID
                FROM `order` o
                JOIN retailshop s ON o.ShopID = s.ShopID
                LEFT JOIN order_details od ON o.OrderID = od.OrderID
                WHERE o.OrderID = %s
                GROUP BY o.OrderID, o.OrderDate, o.OrderStatus, o.ShopID, s.ShopName, o.WarehouseID
            """, (id,))
            order = cursor.fetchone()
            
            if not order:
                flash("Order not found", "error")
                return redirect('/shop/orders')

            # Get product details with unit from product table
            cursor.execute("""
                SELECT od.OrderID, od.ProductID, od.OrderQuantity, p.Unit, p.ProductName
                FROM order_details od
                JOIN product p ON od.ProductID = p.ProductID
                WHERE od.OrderID = %s
            """, (id,))
            products = cursor.fetchall()

            # Get all shops for dropdown
            cursor.execute("SELECT ShopID, ShopName FROM retailshop")
            shops = cursor.fetchall()

            # Get all products for dropdown
            cursor.execute("SELECT ProductID, ProductName FROM product")
            all_products = cursor.fetchall()

            # Get all warehouses for dropdown
            cursor.execute("SELECT WarehouseID, Name FROM warehouse")
            warehouses = cursor.fetchall()

            return render_template('retail_shop/order/edit.html', 
                                 order=order, 
                                 order_products=products,
                                 shops=shops,
                                 all_products=all_products,
                                 warehouses=warehouses)

        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect('/shop/orders')
        finally:
            cursor.close()
            conn.close()

    elif request.method == 'POST':
        try:
            shop_id = request.form.get('shop_id')
            status = request.form.get('status')
            warehouse_id = request.form.get('warehouse_id') if status == 'Accepted' else None
            product_ids = request.form.getlist('product_id[]')
            quantities = request.form.getlist('quantity[]')

            # Start transaction
            conn.begin()
            
            # Update order
            if warehouse_id:
                cursor.execute("""
                    UPDATE `order` 
                    SET ShopID = %s, OrderStatus = %s, WarehouseID = %s
                    WHERE OrderID = %s
                """, (shop_id, status, warehouse_id, id))
            else:
                cursor.execute("""
                    UPDATE `order` 
                    SET ShopID = %s, OrderStatus = %s, WarehouseID = NULL
                    WHERE OrderID = %s
                """, (shop_id, status, id))

            # Delete existing order details
            cursor.execute("DELETE FROM order_details WHERE OrderID = %s", (id,))

            # Insert new order details
            for i in range(len(product_ids)):
                if product_ids[i] and quantities[i]:  # Only insert if product and quantity are provided
                    cursor.execute("""
                        INSERT INTO order_details (OrderID, ProductID, OrderQuantity)
                        VALUES (%s, %s, %s)
                    """, (id, product_ids[i], quantities[i]))

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

@shop_routes.route('/shop/orders/delete/<int:id>')
@login_required
def delete_order(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete order details first (due to foreign key constraint)
        cursor.execute("DELETE FROM order_details WHERE OrderID = %s", (id,))
        # Then delete the main order
        cursor.execute("DELETE FROM `order` WHERE OrderID = %s", (id,))
        conn.commit()
        flash("Order deleted successfully!", "success")
    except Exception as e:
        conn.rollback()
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
