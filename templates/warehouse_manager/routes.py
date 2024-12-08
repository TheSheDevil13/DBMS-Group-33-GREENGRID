from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, session
import pymysql
from functools import wraps

# Create the blueprint for warehouse manager routes
warehouse_manager_routes = Blueprint('warehouse_manager', __name__)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'W':
            flash('Please log in as a warehouse manager to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='greengrid',
    )

# Warehouse Manager Dashboard
@warehouse_manager_routes.route('/warehouse-manager/manager-dashboard')
@login_required
def manager_dashboard():
    return render_template('warehouse_manager/dashboard/dashboard.html')

# Stock Products
@warehouse_manager_routes.route('/warehouse-manager/stock-products')
@login_required
def stock_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                s.StockID,
                s.StockQuantity,
                s.StockUnit,
                s.LastUpdateDate,
                s.StockAvailability,
                w.City as WarehouseName,
                p.ProductName,
                s.WarehouseID,
                s.ProductID
            FROM stock s
            JOIN warehouse w ON s.WarehouseID = w.WarehouseID
            JOIN product p ON s.ProductID = p.ProductID
            ORDER BY s.StockID DESC
        """)
        stocks = cursor.fetchall()
        return render_template('warehouse_manager/stock-product/list.html', stocks=stocks)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect('/warehouse-manager/manager-dashboard')
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/stock-products/create', methods=['GET', 'POST'])
@login_required
def create_stock():
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT WarehouseID, City FROM warehouse")
            warehouses = cursor.fetchall()
            cursor.execute("SELECT ProductID, ProductName FROM product")
            products = cursor.fetchall()
            return render_template('warehouse_manager/stock-product/create.html', 
                                warehouses=warehouses, products=products)
        except Exception as e:
            flash(f"Error loading data: {e}", "error")
            return redirect(url_for('warehouse_manager.stock_products'))
        finally:
            cursor.close()
            conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        warehouse_id = request.form['warehouse_id']
        product_id = request.form['product_id']
        stock_quantity = request.form['stock_quantity']
        stock_unit = request.form['stock_unit']
        
        # Set StockAvailability based on quantity
        stock_availability = 'In Stock' if float(stock_quantity) > 0 else 'Out of Stock'
        
        cursor.execute("""
            INSERT INTO stock (WarehouseID, ProductID, StockQuantity, StockUnit, LastUpdateDate, StockAvailability) 
            VALUES (%s, %s, %s, %s, CURDATE(), %s)
        """, (warehouse_id, product_id, stock_quantity, stock_unit, stock_availability))
        conn.commit()
        flash("Stock added successfully!", "success")
        return redirect(url_for('warehouse_manager.stock_products'))
    except Exception as e:
        conn.rollback()
        flash(f"Error adding stock: {e}", "error")
        return redirect(url_for('warehouse_manager.create_stock'))
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/stock-products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_stock(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        try:
            cursor.execute("""
                SELECT s.*, w.City, p.ProductName 
                FROM stock s
                JOIN warehouse w ON s.WarehouseID = w.WarehouseID
                JOIN product p ON s.ProductID = p.ProductID
                WHERE s.StockID = %s
            """, (id,))
            stock = cursor.fetchone()
            cursor.execute("SELECT WarehouseID, City FROM warehouse")
            warehouses = cursor.fetchall()
            cursor.execute("SELECT ProductID, ProductName FROM product")
            products = cursor.fetchall()
            
            if stock:
                return render_template('warehouse_manager/stock-product/edit.html', 
                                    stock=stock, warehouses=warehouses, products=products)
            flash("Stock not found!", "error")
            return redirect(url_for('warehouse_manager.stock_products'))
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('warehouse_manager.stock_products'))
        finally:
            cursor.close()
            conn.close()
    
    try:
        warehouse_id = request.form['warehouse_id']
        product_id = request.form['product_id']
        stock_quantity = request.form['stock_quantity']
        stock_unit = request.form['stock_unit']
        
        # Set StockAvailability based on quantity
        stock_availability = 'In Stock' if float(stock_quantity) > 0 else 'Out of Stock'
        
        cursor.execute("""
            UPDATE stock 
            SET WarehouseID = %s, ProductID = %s, StockQuantity = %s, 
                StockUnit = %s, LastUpdateDate = CURDATE(), StockAvailability = %s
            WHERE StockID = %s
        """, (warehouse_id, product_id, stock_quantity, stock_unit, stock_availability, id))
        conn.commit()
        flash("Stock updated successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error updating stock: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('warehouse_manager.stock_products'))

@warehouse_manager_routes.route('/warehouse-manager/stock-products/delete/<int:id>')
@login_required
def delete_stock(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM stock WHERE StockID = %s", (id,))
        conn.commit()
        flash("Stock deleted successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting stock: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('warehouse_manager.stock_products'))

# Dispatch Management Routes
@warehouse_manager_routes.route('/warehouse-manager/dispatches')
@login_required
def list_dispatches():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT 
                d.WarehouseID,
                d.ShopID,
                d.DispatchQuantity,
                d.DispatchUnit,
                d.DispatchDate,
                o.OrderID,
                rs.ShopName,
                o.OrderStatus
            FROM dispatch d
            JOIN `order` o ON d.WarehouseID = o.WarehouseID AND d.ShopID = o.ShopID
            JOIN retailshop rs ON d.ShopID = rs.ShopID
            WHERE d.WarehouseID = %s
            ORDER BY d.DispatchDate DESC
        """, (session.get('warehouse_id'),))
        dispatches = cursor.fetchall()
        return render_template('warehouse_manager/dispatch/list.html', dispatches=dispatches)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect('/warehouse-manager/manager-dashboard')
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/dispatch/create', methods=['GET', 'POST'])
@login_required
def create_dispatch():
    if request.method == 'POST':
        order_id = request.form.get('order')
        product_ids = request.form.getlist('product_ids[]')
        quantities = request.form.getlist('quantities[]')
        units = request.form.getlist('units[]')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Start transaction
            conn.begin()
            
            # Get order details
            cursor.execute("""
                SELECT WarehouseID, ShopID 
                FROM `order`
                WHERE OrderID = %s
            """, (order_id,))
            order = cursor.fetchone()
            
            # Update order status to Delivered
            cursor.execute("""
                UPDATE `order`
                SET OrderStatus = 'Delivered' 
                WHERE OrderID = %s
            """, (order_id,))
            
            # Create dispatch entries
            for i in range(len(product_ids)):
                cursor.execute("""
                    INSERT INTO dispatch 
                    (WarehouseID, ShopID, DispatchQuantity, DispatchUnit, DispatchDate)
                    VALUES (%s, %s, %s, %s, CURDATE())
                """, (order[0], order[1], quantities[i], units[i]))
                
                # Update stock quantity
                cursor.execute("""
                    UPDATE stock 
                    SET StockQuantity = StockQuantity - %s 
                    WHERE WarehouseID = %s AND ProductID = %s
                """, (quantities[i], order[0], product_ids[i]))
            
            conn.commit()
            flash("Dispatch created successfully!", "success")
            return redirect(url_for('warehouse_manager.list_dispatches'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "error")
            return redirect(url_for('warehouse_manager.create_dispatch'))
        finally:
            cursor.close()
            conn.close()
    else:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT 
                    o.OrderID,
                    o.OrderDate,
                    rs.ShopName,
                    rs.ShopID,
                    o.OrderStatus
                FROM `order` o
                JOIN retailshop rs ON o.ShopID = rs.ShopID
                WHERE o.WarehouseID = %s AND o.OrderStatus = 'Accepted'
                ORDER BY o.OrderDate DESC
            """, (session.get('warehouse_id'),))
            orders = cursor.fetchall()
            
            if not orders:
                flash("No accepted orders available for dispatch.", "info")
                return redirect(url_for('warehouse_manager.list_dispatches'))
                
            return render_template('warehouse_manager/dispatch/create.html', orders=orders)
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('warehouse_manager.list_dispatches'))
        finally:
            cursor.close()
            conn.close()

@warehouse_manager_routes.route('/warehouse-manager/get-order-details')
@login_required
def get_order_details():
    order_id = request.args.get('order_id')
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT 
                od.ProductID,
                p.ProductName as product_name,
                od.OrderQuantity as ordered_quantity,
                od.Unit as unit,
                s.StockQuantity as available_quantity
            FROM order_details od
            JOIN product p ON od.ProductID = p.ProductID
            JOIN `order` o ON od.OrderID = o.OrderID
            LEFT JOIN stock s ON od.ProductID = s.ProductID AND o.WarehouseID = s.WarehouseID
            WHERE od.OrderID = %s
        """, (order_id,))
        products = cursor.fetchall()
        return jsonify({'products': products})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Settings
@warehouse_manager_routes.route('/warehouse-manager/settings')
@login_required
def settings():
    return render_template('warehouse_manager/settings/settings.html')

# Warehouse Management Routes
@warehouse_manager_routes.route('/warehouse-manager/warehouses')
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
        return render_template('warehouse_manager/warehouse-management/list.html', warehouses=warehouses)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect('/warehouse-manager/manager-dashboard')
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/warehouses/create', methods=['GET', 'POST'])
@login_required
def create_warehouse():
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT UserID, Username FROM users WHERE Role = 'W'")
            employees = cursor.fetchall()
            return render_template('warehouse_manager/warehouse-management/create.html', employees=employees)
        except Exception as e:
            flash(f"Error loading employees: {e}", "error")
            return redirect(url_for('warehouse_manager.list_warehouses'))
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
            return redirect(url_for('warehouse_manager.create_warehouse'))
        
        employee_id = request.form['employee_id']
        
        # Validate data
        if not name or len(name.strip()) == 0:
            flash("Warehouse name is required", "error")
            return redirect(url_for('warehouse_manager.create_warehouse'))
            
        if len(postal_code) != 6:
            flash("Postal code must be exactly 6 characters long", "error")
            return redirect(url_for('warehouse_manager.create_warehouse'))
            
        # Validate decimal ranges
        if not (-999.99 <= temperature <= 999.99):
            flash("Temperature must be between -999.99 and 999.99", "error")
            return redirect(url_for('warehouse_manager.create_warehouse'))
            
        if not (0 <= humidity <= 100):
            flash("Humidity must be between 0 and 100", "error")
            return redirect(url_for('warehouse_manager.create_warehouse'))
            
        if not (0 <= light_exposure <= 9999.99):
            flash("Light exposure must be between 0 and 9999.99", "error")
            return redirect(url_for('warehouse_manager.create_warehouse'))
        
        # Validate employee exists and has role 'W'
        cursor.execute("SELECT UserID FROM users WHERE UserID = %s AND Role = 'W'", (employee_id,))
        if not cursor.fetchone():
            flash("Invalid warehouse employee selected", "error")
            return redirect(url_for('warehouse_manager.create_warehouse'))
        
        # Insert new warehouse
        cursor.execute("""
            INSERT INTO warehouse (Name, Street, City, PostalCode, Temperature, Humidity, LightExposure, WEmployeeID) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, street, city, postal_code, temperature, humidity, light_exposure, employee_id))
        conn.commit()
        flash("New warehouse added successfully!", "success")
        return redirect(url_for('warehouse_manager.list_warehouses'))
    except Exception as e:
        conn.rollback()
        flash(f"Error adding warehouse: {e}", "error")
        return redirect(url_for('warehouse_manager.create_warehouse'))
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/warehouses/edit/<int:id>', methods=['GET', 'POST'])
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
                return render_template('warehouse_manager/warehouse-management/edit.html', 
                                    warehouse=warehouse, employees=employees)
            flash("Warehouse not found!", "error")
            return redirect(url_for('warehouse_manager.list_warehouses'))
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('warehouse_manager.list_warehouses'))
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
            return redirect(url_for('warehouse_manager.edit_warehouse', id=id))
        
        employee_id = request.form['employee_id']
        
        # Validate data
        if not name or len(name.strip()) == 0:
            flash("Warehouse name is required", "error")
            return redirect(url_for('warehouse_manager.edit_warehouse', id=id))
            
        if len(postal_code) != 6:
            flash("Postal code must be exactly 6 characters long", "error")
            return redirect(url_for('warehouse_manager.edit_warehouse', id=id))
            
        # Validate decimal ranges
        if not (-999.99 <= temperature <= 999.99):
            flash("Temperature must be between -999.99 and 999.99", "error")
            return redirect(url_for('warehouse_manager.edit_warehouse', id=id))
            
        if not (0 <= humidity <= 100):
            flash("Humidity must be between 0 and 100", "error")
            return redirect(url_for('warehouse_manager.edit_warehouse', id=id))
            
        if not (0 <= light_exposure <= 9999.99):
            flash("Light exposure must be between 0 and 9999.99", "error")
            return redirect(url_for('warehouse_manager.edit_warehouse', id=id))
        
        # Validate employee exists and has role 'W'
        cursor.execute("SELECT UserID FROM users WHERE UserID = %s AND Role = 'W'", (employee_id,))
        if not cursor.fetchone():
            flash("Invalid warehouse employee selected", "error")
            return redirect(url_for('warehouse_manager.edit_warehouse', id=id))
        
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
        return redirect(url_for('warehouse_manager.list_warehouses'))
    except Exception as e:
        conn.rollback()
        flash(f"Error updating warehouse: {e}", "error")
        return redirect(url_for('warehouse_manager.edit_warehouse', id=id))
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/warehouses/delete/<int:id>')
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
    return redirect(url_for('warehouse_manager.list_warehouses'))

# Product Management Routes Starts
@warehouse_manager_routes.route('/warehouse-manager/products')
@login_required
def list_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        return render_template('warehouse_manager/product/list.html', products=products)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect('/warehouse-manager/manager-dashboard')
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'GET':
        return render_template('warehouse_manager/product/create.html')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get form data
        product_name = request.form['product_name']
        category = request.form['category']
        price_per_unit = request.form['price_per_unit']
        seasonality = request.form['seasonality']
        
        # Insert new product
        cursor.execute("""
            INSERT INTO product (ProductName, Category, PricePerUnit, Seasonality) 
            VALUES (%s, %s, %s, %s)
        """, (product_name, category, price_per_unit, seasonality))
        conn.commit()
        flash("New product added successfully!", "success")
        return redirect(url_for('warehouse_manager.list_products'))
    except Exception as e:
        conn.rollback()
        flash(f"Error adding product: {e}", "error")
        return redirect(url_for('warehouse_manager.create_product'))
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM product WHERE ProductID = %s", (id,))
            product = cursor.fetchone()
            if product:
                return render_template('warehouse_manager/product/edit.html', product=product)
            flash("Product not found!", "error")
            return redirect(url_for('warehouse_manager.list_products'))
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('warehouse_manager.list_products'))
        finally:
            cursor.close()
            conn.close()
    
    try:
        # Get form data
        product_name = request.form['product_name']
        category = request.form['category']
        price_per_unit = request.form['price_per_unit']
        seasonality = request.form['seasonality']
        
        # Update product
        cursor.execute("""
            UPDATE product 
            SET ProductName = %s, Category = %s, PricePerUnit = %s, Seasonality = %s
            WHERE ProductID = %s
        """, (product_name, category, price_per_unit, seasonality, id))
        conn.commit()
        flash("Product updated successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error updating product: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('warehouse_manager.list_products'))

@warehouse_manager_routes.route('/warehouse-manager/products/delete/<int:id>', methods=['POST'])
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
    return redirect(url_for('warehouse_manager.list_products'))
# Product Management Routes Ends

# Shop Management Routes
@warehouse_manager_routes.route('/warehouse-manager/shops')
@login_required
def list_shops():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM retailshop ORDER BY ShopID DESC")
        shops = cursor.fetchall()
        return render_template('warehouse_manager/shop/list.html', shops=shops)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect('/warehouse-manager/manager-dashboard')
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/shops/create', methods=['GET', 'POST'])
@login_required
def create_shop():
    if request.method == 'GET':
        return render_template('warehouse_manager/shop/create.html')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        shop_name = request.form['shop_name']
        number = request.form['number']
        email = request.form['email']
        street = request.form['street']
        city = request.form['city']
        postal_code = request.form['postal_code']
        
        cursor.execute("""
            INSERT INTO retailshop (ShopName, Number, Email, Street, City, PostalCode)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (shop_name, number, email, street, city, postal_code))
        conn.commit()
        flash("Shop added successfully!", "success")
        return redirect(url_for('warehouse_manager.list_shops'))
    except Exception as e:
        conn.rollback()
        flash(f"Error adding shop: {e}", "error")
        return redirect(url_for('warehouse_manager.create_shop'))
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/shops/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_shop(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM retailshop WHERE ShopID = %s", (id,))
            shop = cursor.fetchone()
            if shop:
                return render_template('warehouse_manager/shop/edit.html', shop=shop)
            flash("Shop not found!", "error")
            return redirect(url_for('warehouse_manager.list_shops'))
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('warehouse_manager.list_shops'))
        finally:
            cursor.close()
            conn.close()
    
    try:
        shop_name = request.form['shop_name']
        number = request.form['number']
        email = request.form['email']
        street = request.form['street']
        city = request.form['city']
        postal_code = request.form['postal_code']
        
        cursor.execute("""
            UPDATE retailshop 
            SET ShopName = %s, Number = %s, Email = %s, 
                Street = %s, City = %s, PostalCode = %s
            WHERE ShopID = %s
        """, (shop_name, number, email, street, city, postal_code, id))
        conn.commit()
        flash("Shop updated successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error updating shop: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('warehouse_manager.list_shops'))

@warehouse_manager_routes.route('/warehouse-manager/shops/delete/<int:id>')
@login_required
def delete_shop(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM retailshop WHERE ShopID = %s", (id,))
        conn.commit()
        flash("Shop deleted successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting shop: {e}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('warehouse_manager.list_shops'))

# Order Management Routes
@warehouse_manager_routes.route('/warehouse-manager/orders')
@login_required
def list_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get orders with shop details and product count
        cursor.execute("""
            SELECT o.OrderID, o.OrderDate, o.OrderStatus, o.ShopID, s.ShopName,
                   COUNT(od.ProductID) as product_count
            FROM `order` o
            JOIN retailshop s ON o.ShopID = s.ShopID
            LEFT JOIN order_details od ON o.OrderID = od.OrderID
            GROUP BY o.OrderID, o.OrderDate, o.OrderStatus, o.ShopID, s.ShopName
            ORDER BY o.OrderID DESC
        """)
        orders = list(cursor.fetchall())  # Convert to list to allow modification

        # Get product details for each order
        for i, order in enumerate(orders):
            cursor.execute("""
                SELECT od.OrderID, od.ProductID, od.OrderQuantity, od.Unit, p.ProductName
                FROM order_details od
                JOIN product p ON od.ProductID = p.ProductID
                WHERE od.OrderID = %s
            """, (order[0],))
            # Add products as the last element of the order tuple
            orders[i] = order + (cursor.fetchall(),)

        return render_template('warehouse_manager/order/list.html', orders=orders)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect('/warehouse-manager/manager-dashboard')
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/orders/create', methods=['GET', 'POST'])
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
            
            return render_template('warehouse_manager/order/create.html', 
                                products=products, shops=shops)
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('warehouse_manager.list_orders'))
        finally:
            cursor.close()
            conn.close()
    
    try:
        # Get form data
        shop_id = request.form['shop_id']
        order_status = request.form['order_status']
        products = request.form.getlist('products[]')
        quantities = request.form.getlist('quantities[]')
        units = request.form.getlist('units[]')

        # Insert main order
        cursor.execute("""
            INSERT INTO `order` (OrderDate, OrderStatus, ShopID)
            VALUES (CURDATE(), %s, %s)
        """, (order_status, shop_id))
        
        order_id = cursor.lastrowid

        # Insert order details
        for i in range(len(products)):
            cursor.execute("""
                INSERT INTO order_details (OrderID, ProductID, OrderQuantity, Unit)
                VALUES (%s, %s, %s, %s)
            """, (order_id, products[i], quantities[i], units[i]))

        conn.commit()
        flash("Order created successfully!", "success")
        return redirect(url_for('warehouse_manager.list_orders'))
    except Exception as e:
        conn.rollback()
        flash(f"Error creating order: {e}", "error")
        return redirect(url_for('warehouse_manager.create_order'))
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/orders/edit/<int:id>', methods=['GET', 'POST'])
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
                return redirect('/warehouse-manager/orders')

            # Get product details
            cursor.execute("""
                SELECT od.OrderID, od.ProductID, od.OrderQuantity, od.Unit, p.ProductName
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

            return render_template('warehouse_manager/order/edit.html', 
                                 order=order, 
                                 order_products=products,
                                 shops=shops,
                                 all_products=all_products,
                                 warehouses=warehouses)

        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect('/warehouse-manager/orders')
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
            units = request.form.getlist('unit[]')

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
                        INSERT INTO order_details (OrderID, ProductID, OrderQuantity, Unit)
                        VALUES (%s, %s, %s, %s)
                    """, (id, product_ids[i], quantities[i], units[i]))

            conn.commit()
            flash("Order updated successfully", "success")
            return redirect(url_for('warehouse_manager.list_orders'))

        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "error")
            return redirect(url_for('warehouse_manager.edit_order', id=id))
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('warehouse_manager.list_orders'))

@warehouse_manager_routes.route('/warehouse-manager/orders/delete/<int:id>')
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
    return redirect(url_for('warehouse_manager.list_orders'))

@warehouse_manager_routes.route('/warehouse-manager/orders/view/<int:id>')
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
            return redirect('/warehouse-manager/orders')

        # Get product details
        cursor.execute("""
            SELECT p.ProductName, od.OrderQuantity, od.Unit
            FROM order_details od
            JOIN product p ON od.ProductID = p.ProductID
            WHERE od.OrderID = %s
        """, (id,))
        products = cursor.fetchall()
        
        # Add products to the order tuple
        order = order + (products,)

        return render_template('warehouse_manager/order/details.html', order=order)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect('/warehouse-manager/orders')
    finally:
        cursor.close()
        conn.close()
