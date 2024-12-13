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
def dashboard():
    return render_template('agricultural_analyst/dashboard/analyst-dashboard.html')

@analyst_routes.route('/agricultural-analyst/production-data')
@login_required
def production_data():
    # Fetch production data with farmer and product information
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.*,
            f.FarmerName,
            pr.ProductName,
            pr.Category
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
        farmer_id = request.form.get('farmer_id')
        product_id = request.form.get('product_id')
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO productiondata 
                (HarvestDate, ProductionCost, ShelfLife, Acreage, YieldRate, FarmerID, ProductID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (harvest_date, production_cost, shelf_life, acreage, yield_rate, farmer_id, product_id))
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
        farmer_id = request.form.get('farmer_id')
        product_id = request.form.get('product_id')
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE productiondata 
                SET HarvestDate=%s, ProductionCost=%s, ShelfLife=%s, Acreage=%s, 
                    YieldRate=%s, FarmerID=%s, ProductID=%s
                WHERE ProductionID=%s
            """, (harvest_date, production_cost, shelf_life, acreage, yield_rate, 
                  farmer_id, product_id, id))
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
            pr.Category
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
    try:
        # Delete the production data
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM productiondata WHERE ProductionID = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
