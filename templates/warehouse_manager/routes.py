from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, session
import pymysql
from functools import wraps

# Create the blueprint for warehouse manager routes
warehouse_manager_routes = Blueprint('warehouse_manager', __name__)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Debug - Login Required: Checking authorization")
        print(f"Debug - Login Required: Session contents: {session}")
        print(f"Debug - Login Required: user_id in session: {'user_id' in session}")
        print(f"Debug - Login Required: role: {session.get('role')}")
        print(f"Debug - Login Required: warehouse_id: {session.get('warehouse_id')}")
        
        if 'user_id' not in session:
            print("Debug - Login Required: No user_id in session")
            return redirect('/login')
        if session.get('role') != 'W':
            print(f"Debug - Login Required: Invalid role: {session.get('role')}")
            return redirect('/login')
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
    print("\nDebug - Manager Dashboard: Function entry")
    print(f"Debug - Manager Dashboard: Full session data: {session}")
    print(f"Debug - Manager Dashboard: user_id: {session.get('user_id')}")
    print(f"Debug - Manager Dashboard: warehouse_id: {session.get('warehouse_id')}")
    print(f"Debug - Manager Dashboard: role: {session.get('role')}")
    
    if not session.get('warehouse_id'):
        print("Debug - Manager Dashboard: No warehouse_id in session")
        flash('No warehouse assigned to this manager', 'error')
        return redirect('/login')
        
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    data = {}
    
    try:
        # Get warehouse and manager details
        cursor.execute("""
            SELECT 
                w.*,
                CONCAT(e.FirstName, ' ', e.LastName) as ManagerName,
                e.Email as ManagerEmail
            FROM warehouse w
            JOIN users e ON w.WEmployeeID = e.UserID
            WHERE w.WEmployeeID = %s
        """, (session.get('user_id'),))
        data['warehouse_info'] = cursor.fetchone()
        
        if not data['warehouse_info']:
            flash('Could not find warehouse information', 'error')
            return redirect('/login')
        
        # Get top 5 products by current stock
        cursor.execute("""
            SELECT 
                p.ProductName,
                SUM(CASE 
                    WHEN s.StockAvailability = 'Incoming' THEN s.StockQuantity 
                    WHEN s.StockAvailability = 'Outgoing' THEN -s.StockQuantity 
                    ELSE 0 
                END) as CurrentStock,
                p.Unit
            FROM stock s
            JOIN product p ON s.ProductID = p.ProductID
            WHERE s.WarehouseID = %s
            GROUP BY p.ProductID, p.ProductName, p.Unit
            HAVING CurrentStock > 0
            ORDER BY CurrentStock DESC
            LIMIT 5
        """, (session.get('warehouse_id'),))
        data['top_products'] = cursor.fetchall()
        
        # Get dispatch counts for last 6 months
        cursor.execute("""
            SELECT 
                MONTH(DispatchDate) as MonthNum,
                COUNT(*) as DispatchCount
            FROM dispatch 
            WHERE WarehouseID = %s 
            AND DispatchDate >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
            GROUP BY MONTH(DispatchDate)
            ORDER BY MonthNum
        """, (session.get('warehouse_id'),))
        monthly_data = cursor.fetchall()
        
        # Convert month numbers to names
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
        data['monthly_dispatches'] = [
            {'Month': months[d['MonthNum']-1], 'DispatchCount': d['DispatchCount']} 
            for d in monthly_data
        ]
        
        # Get daily stock movements for last 7 days per product
        cursor.execute("""
            SELECT 
                DATE(s.LastUpdateDate) as Date,
                p.ProductID,
                p.ProductName,
                p.Unit,
                s.StockAvailability,
                SUM(s.StockQuantity) as Quantity
            FROM stock s
            JOIN product p ON s.ProductID = p.ProductID
            WHERE s.WarehouseID = %s 
            AND s.LastUpdateDate >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
            GROUP BY DATE(s.LastUpdateDate), p.ProductID, p.ProductName, p.Unit, s.StockAvailability
            ORDER BY s.LastUpdateDate, p.ProductID
        """, (session.get('warehouse_id'),))
        movements = cursor.fetchall()
        
        # Process stock movements to get running totals per product
        products = {}
        dates = set()
        
        # First, collect all unique dates and products
        for m in movements:
            dates.add(m['Date'].strftime('%Y-%m-%d'))
            if m['ProductID'] not in products:
                products[m['ProductID']] = {
                    'name': m['ProductName'],
                    'unit': m['Unit'],
                    'data': {}
                }
        
        dates = sorted(list(dates))
        
        # Initialize all dates for all products with 0
        for product_id in products:
            running_total = 0
            for date in dates:
                products[product_id]['data'][date] = running_total
        
        # Calculate running totals
        for date in dates:
            for m in movements:
                if m['Date'].strftime('%Y-%m-%d') == date:
                    product_id = m['ProductID']
                    quantity = m['Quantity']
                    if m['StockAvailability'] == 'Incoming':
                        products[product_id]['data'][date] += quantity
                    else:
                        products[product_id]['data'][date] -= quantity
            
            # Carry forward the running total to next date
            for product_id in products:
                if date != dates[-1]:  # If not the last date
                    next_date = dates[dates.index(date) + 1]
                    products[product_id]['data'][next_date] = products[product_id]['data'][date]
        
        # Format data for the chart
        data['stock_movements'] = {
            'dates': dates,
            'products': [
                {
                    'name': product['name'],
                    'unit': product['unit'],
                    'data': list(product['data'].values())
                }
                for product in products.values()
            ]
        }
        
        # Get active orders pending dispatch
        cursor.execute("""
            SELECT 
                o.OrderID,
                o.OrderDate,
                o.OrderStatus,
                rs.ShopName,
                rs.Email as ShopEmail,
                rs.Street as ShopStreet,
                rs.City as ShopCity,
                rs.PostalCode as ShopPostalCode
            FROM `order` o
            JOIN retailshop rs ON o.ShopID = rs.ShopID
            WHERE o.WarehouseID = %s
            AND o.OrderStatus = 'Accepted'
            ORDER BY o.OrderDate DESC
            LIMIT 10
        """, (session.get('warehouse_id'),))
        data['active_orders'] = cursor.fetchall()
        
        return render_template('warehouse_manager/dashboard/dashboard.html', data=data)
    except Exception as e:
        print(f"Debug - Manager Dashboard: Error occurred: {str(e)}")  # Debug print
        flash(f"Error loading dashboard: {str(e)}", "error")
        return redirect('/login')
    finally:
        cursor.close()
        conn.close()

# Stock Products
@warehouse_manager_routes.route('/warehouse-manager/stock-products')
@login_required
def stock_products():
    print("\n=== Debug Stock Products ===")
    print(f"Session data: {session}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        warehouse_filter = ""
        params = []
        if 'warehouse_id' in session:
            warehouse_filter = "WHERE s.WarehouseID = %s"
            params = [session['warehouse_id']]
            print(f"Using warehouse filter: {warehouse_filter} with params: {params}")
        else:
            print("No warehouse_id in session!")

        # First, let's check if we have any stock data at all
        cursor.execute("SELECT COUNT(*) FROM stock")
        total_stock_count = cursor.fetchone()[0]
        print(f"Total stock records in database: {total_stock_count}")

        # Query for individual stocks
        stock_query = f"""
            SELECT 
                s.StockID,
                s.StockQuantity,
                p.Unit as StockUnit,
                s.LastUpdateDate,
                s.StockAvailability,
                w.Name as WarehouseName,
                p.ProductName,
                s.WarehouseID,
                s.ProductID
            FROM stock s
            JOIN warehouse w ON s.WarehouseID = w.WarehouseID
            JOIN product p ON s.ProductID = p.ProductID
            {warehouse_filter}
            ORDER BY s.StockID DESC
        """
        print(f"Executing stock query: {stock_query}")
        print(f"With params: {params}")
        cursor.execute(stock_query, params)
        stocks = cursor.fetchall()
        print(f"Found {len(stocks)} stock records")

        # Query for total stock by product
        total_query = f"""
            SELECT 
                p.ProductID,
                p.ProductName,
                p.Unit,
                SUM(CASE 
                    WHEN s.StockAvailability = 'Incoming' THEN s.StockQuantity 
                    WHEN s.StockAvailability = 'Outgoing' THEN -s.StockQuantity 
                    ELSE 0 
                END) as TotalStock
            FROM product p
            LEFT JOIN stock s ON p.ProductID = s.ProductID
            {warehouse_filter}
            GROUP BY p.ProductID, p.ProductName, p.Unit
            ORDER BY p.ProductName
        """
        print(f"Executing total query: {total_query}")
        print(f"With params: {params}")
        cursor.execute(total_query, params)
        total_stocks = cursor.fetchall()
        print(f"Found {len(total_stocks)} total stock records")

        return render_template('warehouse_manager/stock-product/list.html', 
                            stocks=stocks, 
                            total_stocks=total_stocks)
    except Exception as e:
        print(f"Error in stock_products: {str(e)}")
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
            cursor.execute("SELECT ProductID, ProductName FROM product")
            products = cursor.fetchall()
            return render_template('warehouse_manager/stock-product/create.html', 
                                products=products)
        except Exception as e:
            flash(f"Error loading data: {e}", "error")
            return redirect(url_for('warehouse_manager.stock_products'))
        finally:
            cursor.close()
            conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get warehouse_id from session instead of form
        warehouse_id = session.get('warehouse_id')
        if not warehouse_id:
            flash("No warehouse assigned to user!", "error")
            return redirect(url_for('warehouse_manager.stock_products'))

        product_id = request.form['product_id']
        stock_quantity = request.form['stock_quantity']
        
        # Set StockAvailability based on quantity
        stock_availability = 'Incoming'
        
        print(f"Debug - Creating stock: warehouse_id={warehouse_id}, product_id={product_id}, quantity={stock_quantity}")
        cursor.execute("""
            INSERT INTO stock (WarehouseID, ProductID, StockQuantity, LastUpdateDate, StockAvailability) 
            VALUES (%s, %s, %s, CURDATE(), %s)
        """, (warehouse_id, product_id, stock_quantity, stock_availability))
        conn.commit()
        flash("Stock added successfully!", "success")
        return redirect(url_for('warehouse_manager.stock_products'))
    except Exception as e:
        print(f"Debug - Error creating stock: {str(e)}")
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
                SELECT 
                    s.StockID,
                    s.WarehouseID,
                    s.ProductID,
                    s.StockQuantity,
                    s.StockAvailability,
                    s.LastUpdateDate,
                    w.Name as WarehouseName,
                    p.ProductName,
                    p.Unit as StockUnit
                FROM stock s
                JOIN warehouse w ON s.WarehouseID = w.WarehouseID
                JOIN product p ON s.ProductID = p.ProductID
                WHERE s.StockID = %s
            """, (id,))
            stock = cursor.fetchone()
            cursor.execute("SELECT WarehouseID, Name FROM warehouse")
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
        
        cursor.execute("""
            UPDATE stock 
            SET WarehouseID = %s, ProductID = %s, StockQuantity = %s, 
                LastUpdateDate = CURDATE()
            WHERE StockID = %s
        """, (warehouse_id, product_id, stock_quantity, id))
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
        # Query for accepted orders
        warehouse_filter = ""
        params = []
        if 'warehouse_id' in session:
            warehouse_filter = "AND o.WarehouseID = %s"
            params = [session['warehouse_id']]

        cursor.execute(f"""
            SELECT 
                o.OrderID,
                o.OrderDate,
                o.OrderStatus,
                rs.ShopName,
                rs.ShopID
            FROM `order` o
            JOIN retailshop rs ON o.ShopID = rs.ShopID
            WHERE o.OrderStatus = 'Accepted' {warehouse_filter}
            ORDER BY o.OrderDate DESC
        """, params)
        accepted_orders = cursor.fetchall()

        # Query for dispatches
        cursor.execute("""
            SELECT DISTINCT
                d.DispatchID,
                d.WarehouseID,
                d.OrderID,
                d.DispatchDate,
                o.OrderStatus,
                rs.ShopName
            FROM dispatch d
            JOIN `order` o ON d.OrderID = o.OrderID
            JOIN retailshop rs ON o.ShopID = rs.ShopID
            WHERE d.WarehouseID = %s
            ORDER BY d.DispatchDate DESC
        """, (session.get('warehouse_id'),))
        dispatches = cursor.fetchall()
        
        return render_template('warehouse_manager/dispatch/list.html', 
                             dispatches=dispatches,
                             accepted_orders=accepted_orders)
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
            
            # Create dispatch entry
            cursor.execute("""
                INSERT INTO dispatch 
                (WarehouseID, OrderID, DispatchDate)
                VALUES (%s, %s, CURDATE())
            """, (order[0], order_id))
            
            # Create stock entries for each product
            for i in range(len(product_ids)):
                cursor.execute("""
                    INSERT INTO stock 
                    (StockQuantity, LastUpdateDate, StockAvailability, WarehouseID, ProductID)
                    VALUES (%s, CURDATE(), 'Outgoing', %s, %s)
                """, (quantities[i], order[0], product_ids[i]))
            
            # Update order status to Delivered
            cursor.execute("""
                UPDATE `order`
                SET OrderStatus = 'Delivered' 
                WHERE OrderID = %s
            """, (order_id,))
            
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

@warehouse_manager_routes.route('/warehouse-manager/dispatch/view/<int:id>')
@login_required
def view_dispatch(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # Get dispatch details
        cursor.execute("""
            SELECT 
                d.DispatchID,
                d.WarehouseID,
                d.OrderID,
                d.DispatchDate,
                o.OrderStatus,
                rs.ShopName,
                CONCAT(rs.Street, ', ', rs.City, ' ', rs.PostalCode) as ShopAddress,
                o.OrderDate
            FROM dispatch d
            JOIN `order` o ON d.OrderID = o.OrderID
            JOIN retailshop rs ON o.ShopID = rs.ShopID
            WHERE d.DispatchID = %s AND d.WarehouseID = %s
        """, (id, session.get('warehouse_id')))
        dispatch = cursor.fetchone()
        
        if not dispatch:
            flash("Dispatch not found.", "error")
            return redirect(url_for('warehouse_manager.list_dispatches'))
        
        # Get dispatched products
        cursor.execute("""
            SELECT 
                p.ProductName,
                p.ProductID,
                p.Unit,
                s.StockQuantity as DispatchQuantity
            FROM stock s
            JOIN product p ON s.ProductID = p.ProductID
            WHERE s.WarehouseID = %s 
            AND s.StockAvailability = 'Outgoing'
            AND EXISTS (
                SELECT 1 FROM dispatch d 
                WHERE d.DispatchID = %s 
                AND DATE(s.LastUpdateDate) = d.DispatchDate
            )
        """, (session.get('warehouse_id'), id))
        products = cursor.fetchall()
            
        return render_template('warehouse_manager/dispatch/view.html', 
                             dispatch=dispatch,
                             products=products)
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect(url_for('warehouse_manager.list_dispatches'))
    finally:
        cursor.close()
        conn.close()

@warehouse_manager_routes.route('/warehouse-manager/get-product-unit/<int:product_id>')
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

# Settings
@warehouse_manager_routes.route('/warehouse-manager/settings', methods=['GET', 'POST'])
@login_required
def settings():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        if request.method == 'POST':
            # Get form data
            name = request.form.get('name')
            street = request.form.get('street')
            city = request.form.get('city')
            postal_code = request.form.get('postal_code')
            temperature = request.form.get('temperature')
            humidity = request.form.get('humidity')
            light_exposure = request.form.get('light_exposure')
            
            # Update warehouse information
            cursor.execute("""
                UPDATE warehouse 
                SET Name = %s,
                    Street = %s,
                    City = %s,
                    PostalCode = %s,
                    Temperature = %s,
                    Humidity = %s,
                    LightExposure = %s
                WHERE WarehouseID = %s
            """, (name, street, city, postal_code, temperature, 
                  humidity, light_exposure, session.get('warehouse_id')))
            
            conn.commit()
            flash('Warehouse information updated successfully!', 'success')
            return redirect(url_for('warehouse_manager.settings'))
        
        # Get current warehouse information
        cursor.execute("""
            SELECT 
                WarehouseID,
                Name,
                Street,
                City,
                PostalCode,
                Temperature,
                Humidity,
                LightExposure
            FROM warehouse 
            WHERE WarehouseID = %s
        """, (session.get('warehouse_id'),))
        
        warehouse = cursor.fetchone()
        return render_template('warehouse_manager/settings/settings.html', warehouse=warehouse)
        
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('warehouse_manager.settings'))
    finally:
        cursor.close()
        conn.close()

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
                SELECT od.OrderID, od.ProductID, od.OrderQuantity, p.Unit, p.ProductName
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
            SELECT p.ProductName, od.OrderQuantity, p.Unit
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
