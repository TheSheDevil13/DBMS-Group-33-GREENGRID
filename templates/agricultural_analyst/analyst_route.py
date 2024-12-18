from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, session
import pymysql
from functools import wraps

# Create the blueprint for warehouse manager routes
analyst_routes = Blueprint('analyst', __name__)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'A':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='greengrid',
    )

@analyst_routes.route('/agricultural-analyst/analyst-dashboard')
@login_required
def analyst_dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = session.get('user_id')

    # Get user information
    cur.execute("""
        SELECT UserID, FirstName, LastName, Username, Email, Role
        FROM users
        WHERE UserID = %s
    """, (user_id,))
    user_info = cur.fetchone()

    # Get total products count
    cur.execute("""
        SELECT COUNT(DISTINCT p.ProductID)
        FROM productiondata pd
        JOIN product p ON pd.ProductID = p.ProductID
    """)
    total_products = cur.fetchone()[0]

    # Get total distinct product categories
    cur.execute("""
        SELECT COUNT(DISTINCT p.Category)
        FROM productiondata pd
        JOIN product p ON pd.ProductID = p.ProductID
    """)
    total_categories = cur.fetchone()[0]

    # Get total farmers
    cur.execute("""
        SELECT COUNT(DISTINCT FarmerID)
        FROM productiondata
    """)
    total_farmers = cur.fetchone()[0]

    # Get production data for charts
    cur.execute("""
        SELECT p.ProductName, SUM(pd.TotalProduction) as total_production,
               p.Category, p.Unit
        FROM productiondata pd
        JOIN product p ON pd.ProductID = p.ProductID
        GROUP BY p.ProductID, p.ProductName, p.Category, p.Unit
        ORDER BY total_production DESC
    """)
    production_chart_data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('agricultural_analyst/dashboard/analyst-dashboard.html',
                         user_info=user_info,
                         total_products=total_products,
                         total_categories=total_categories,
                         total_farmers=total_farmers,
                         production_chart_data=production_chart_data)

@analyst_routes.route('/agricultural-analyst/production-data')
@login_required
def production_data():
    # Fetch production data with farmer and product information
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.ProductionID,
            p.HarvestDate,
            p.ProductionCost,
            p.ShelfLife,
            p.Acreage,
            p.YieldRate,
            p.TotalProduction,
            p.FarmerID,
            p.ProductID,
            f.FarmerName,
            f.Number as FarmerNumber,
            f.Email as FarmerEmail,
            f.Street as FarmerStreet,
            f.City as FarmerCity,
            f.PostalCode as FarmerPostalCode,
            pr.ProductName,
            pr.Category as ProductCategory,
            pr.PricePerUnit,
            pr.Unit,
            pr.Seasonality
        FROM productiondata p
        JOIN farmer f ON p.FarmerID = f.FarmerID
        JOIN product pr ON p.ProductID = pr.ProductID
        ORDER BY p.ProductionID DESC
    """)
    production_data = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('agricultural_analyst/production-data/list.html',
                         production_data=production_data)

@analyst_routes.route('/agricultural-analyst/production-data/create', methods=['GET', 'POST'])
@login_required
def create_production_data():
    if request.method == 'POST':
        # Get form data
        harvest_date = request.form.get('harvest_date')
        production_cost = request.form.get('production_cost')
        shelf_life = request.form.get('shelf_life')
        acreage = request.form.get('acreage')
        yield_rate = request.form.get('yield_rate')
        total_production = request.form.get('total_production')
        farmer_id = request.form.get('farmer_id')
        product_id = request.form.get('product_id')
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO productiondata 
                (HarvestDate, ProductionCost, ShelfLife, Acreage, YieldRate, TotalProduction, FarmerID, ProductID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (harvest_date, production_cost, shelf_life, acreage, yield_rate, total_production, farmer_id, product_id))
            conn.commit()
            flash('Production data created successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error creating production data: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('analyst.production_data'))
    
    # Get farmers and products for dropdowns
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT FarmerID, FarmerName, City, PostalCode 
        FROM farmer 
        ORDER BY FarmerName
    """)
    farmers = cur.fetchall()
    
    cur.execute("""
        SELECT ProductID, ProductName, Category, Unit 
        FROM product 
        ORDER BY ProductName
    """)
    products = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('agricultural_analyst/production-data/create.html', 
                         farmers=farmers, 
                         products=products)

@analyst_routes.route('/agricultural-analyst/production-data/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_production_data(id):
    if request.method == 'POST':
        # Get form data
        harvest_date = request.form.get('harvest_date')
        production_cost = request.form.get('production_cost')
        shelf_life = request.form.get('shelf_life')
        acreage = request.form.get('acreage')
        yield_rate = request.form.get('yield_rate')
        total_production = request.form.get('total_production')
        farmer_id = request.form.get('farmer_id')
        product_id = request.form.get('product_id')
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE productiondata 
                SET HarvestDate=%s, ProductionCost=%s, ShelfLife=%s, Acreage=%s, 
                    YieldRate=%s, TotalProduction=%s, FarmerID=%s, ProductID=%s
                WHERE ProductionID=%s
            """, (harvest_date, production_cost, shelf_life, acreage, yield_rate, 
                  total_production, farmer_id, product_id, id))
            conn.commit()
            flash('Production data updated successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error updating production data: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('analyst.production_data'))
    
    # Get production data
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get production data with related information
    cur.execute("""
        SELECT 
            p.*,
            f.FarmerName,
            pr.ProductName,
            pr.Category,
            pr.Unit
        FROM productiondata p
        JOIN farmer f ON p.FarmerID = f.FarmerID
        JOIN product pr ON p.ProductID = pr.ProductID
        WHERE p.ProductionID = %s
    """, (id,))
    production = cur.fetchone()
    
    if not production:
        cur.close()
        conn.close()
        flash('Production data not found!', 'error')
        return redirect(url_for('analyst.production_data'))
    
    # Get farmers and products for dropdowns
    cur.execute("""
        SELECT FarmerID, FarmerName, City, PostalCode 
        FROM farmer 
        ORDER BY FarmerName
    """)
    farmers = cur.fetchall()
    
    cur.execute("""
        SELECT ProductID, ProductName, Category, Unit 
        FROM product 
        ORDER BY ProductName
    """)
    products = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('agricultural_analyst/production-data/edit.html',
                         production=production,
                         farmers=farmers,
                         products=products)

@analyst_routes.route('/agricultural-analyst/production-data/delete/<int:id>', methods=['POST'])
@login_required
def delete_production_data(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Check if production data exists
        cur.execute("SELECT ProductionID FROM productiondata WHERE ProductionID = %s", (id,))
        if not cur.fetchone():
            return jsonify({'success': False, 'message': 'Production data not found'})
        
        # Delete the production data
        cur.execute("DELETE FROM productiondata WHERE ProductionID = %s", (id,))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cur.close()
        conn.close()

@analyst_routes.route('/agricultural-analyst/production-data/reports')
@login_required
def list_reports():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ReportID, Title, Type, ReportDate
        FROM report
        ORDER BY ReportDate DESC
    """)
    reports = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('agricultural_analyst/production-data/reports/list.html',
                         reports=reports)

@analyst_routes.route('/agricultural-analyst/production-data/reports/create', methods=['GET', 'POST'])
@login_required
def create_report():
    if request.method == 'POST':
        title = request.form.get('title')
        details = request.form.get('details')
        report_type = request.form.get('type')
        report_date = request.form.get('report_date')
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO report (Title, Details, Type, ReportDate)
                VALUES (%s, %s, %s, %s)
            """, (title, details, report_type, report_date))
            conn.commit()
            flash('Report created successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error creating report: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('analyst.list_reports'))
    
    return render_template('agricultural_analyst/production-data/reports/create.html')

@analyst_routes.route('/agricultural-analyst/production-data/reports/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_report(id):
    if request.method == 'POST':
        title = request.form.get('title')
        details = request.form.get('details')
        report_type = request.form.get('type')
        report_date = request.form.get('report_date')
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE report 
                SET Title=%s, Details=%s, Type=%s, ReportDate=%s
                WHERE ReportID=%s
            """, (title, details, report_type, report_date, id))
            conn.commit()
            flash('Report updated successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error updating report: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('analyst.list_reports'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ReportID, Title, Details, Type, ReportDate
        FROM report
        WHERE ReportID = %s
    """, (id,))
    report = cur.fetchone()
    cur.close()
    conn.close()
    
    if not report:
        flash('Report not found!', 'error')
        return redirect(url_for('analyst.list_reports'))
    
    return render_template('agricultural_analyst/production-data/reports/edit.html',
                         report=report)

@analyst_routes.route('/agricultural-analyst/production-data/reports/delete/<int:id>', methods=['POST'])
@login_required
def delete_report(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM report WHERE ReportID = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@analyst_routes.route('/agricultural-analyst/production-data/reports/view/<int:id>')
@login_required
def view_report(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get the report details
    cur.execute("""
        SELECT ReportID, Title, Details, Type, ReportDate
        FROM report
        WHERE ReportID = %s
    """, (id,))
    report = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if not report:
        flash('Report not found!', 'error')
        return redirect(url_for('analyst.list_reports'))
    
    return render_template('agricultural_analyst/production-data/reports/view.html',
                         report=report)

@analyst_routes.route('/agricultural-analyst/dashboard-data')
@login_required
def get_dashboard_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get total production
    cur.execute("""
        SELECT COALESCE(SUM(YieldRate * Acreage), 0) as total_production
        FROM productiondata
    """)
    total_production = cur.fetchone()[0]
    
    # Get average yield rate
    cur.execute("""
        SELECT COALESCE(AVG(YieldRate), 0) as avg_yield
        FROM productiondata
    """)
    avg_yield = cur.fetchone()[0]
    
    # Get average production cost
    cur.execute("""
        SELECT COALESCE(AVG(ProductionCost), 0) as avg_cost
        FROM productiondata
    """)
    avg_cost = cur.fetchone()[0]
    
    # Get average shelf life
    cur.execute("""
        SELECT COALESCE(AVG(ShelfLife), 0) as avg_shelf_life
        FROM productiondata
    """)
    avg_shelf_life = cur.fetchone()[0]
    
    # Get production trends (last 6 months)
    cur.execute("""
        SELECT 
            DATE_FORMAT(HarvestDate, '%Y-%m') as month,
            SUM(YieldRate * Acreage) as production
        FROM productiondata
        WHERE HarvestDate >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
        GROUP BY DATE_FORMAT(HarvestDate, '%Y-%m')
        ORDER BY month
    """)
    production_trends = cur.fetchall()
    
    # Get yield analysis by product category
    cur.execute("""
        SELECT 
            pr.Category,
            AVG(p.YieldRate) as avg_yield
        FROM productiondata p
        JOIN product pr ON p.ProductID = pr.ProductID
        GROUP BY pr.Category
    """)
    yield_by_category = cur.fetchall()
    
    # Get shelf life distribution
    cur.execute("""
        SELECT 
            ShelfLife,
            COUNT(*) as count
        FROM productiondata
        GROUP BY ShelfLife
        ORDER BY ShelfLife
    """)
    shelf_life_dist = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return jsonify({
        'total_production': round(float(total_production), 2),
        'avg_yield': round(float(avg_yield), 2),
        'avg_cost': round(float(avg_cost), 2),
        'avg_shelf_life': round(float(avg_shelf_life), 2),
        'production_trends': {
            'labels': [x[0] for x in production_trends],
            'data': [float(x[1]) for x in production_trends]
        },
        'yield_by_category': {
            'labels': [x[0] for x in yield_by_category],
            'data': [float(x[1]) for x in yield_by_category]
        },
        'shelf_life_dist': {
            'labels': [int(x[0]) for x in shelf_life_dist],
            'data': [int(x[1]) for x in shelf_life_dist]
        }
    })

@analyst_routes.route('/agricultural-analyst/get-product-unit/<int:product_id>')
@login_required
def get_product_unit(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT Unit FROM product WHERE ProductID = %s", (product_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    
    if result:
        return jsonify({'unit': result[0]})
    return jsonify({'unit': ''})

@analyst_routes.route('/agricultural-analyst/settings', methods=['GET', 'POST'])
@login_required
def settings():
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = session.get('user_id')
    message = None

    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        email = request.form.get('email')

        try:
            cur.execute("""
                UPDATE users 
                SET FirstName = %s, LastName = %s, Username = %s, Email = %s
                WHERE UserID = %s
            """, (first_name, last_name, username, email, user_id))
            conn.commit()
            message = {'type': 'success', 'text': 'Profile updated successfully!'}
        except Exception as e:
            conn.rollback()
            message = {'type': 'error', 'text': 'Error updating profile: ' + str(e)}

    # Get current user info
    cur.execute("""
        SELECT UserID, FirstName, LastName, Username, Email, Role
        FROM users
        WHERE UserID = %s
    """, (user_id,))
    user_info = cur.fetchone()
    
    cur.close()
    conn.close()

    return render_template('agricultural_analyst/settings.html',
                         user_info=user_info,
                         message=message)
