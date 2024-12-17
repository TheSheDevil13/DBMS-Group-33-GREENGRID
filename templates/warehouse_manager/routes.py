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





