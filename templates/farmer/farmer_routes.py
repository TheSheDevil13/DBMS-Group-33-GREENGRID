from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, session
from werkzeug.security import generate_password_hash
import pymysql
import sys
from datetime import datetime
from functools import wraps


farmer_routes = Blueprint('farmer', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        if session.get('role') != 'F':
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

@farmer_routes.route('/farmer/farmer-dashboard')
@login_required
def farmer_dashboard():
    return render_template('farmer/dashboard/farmer-dashboard.html')

# Production Data Management Routes
@farmer_routes.route('/farmer/production-data', methods=['GET'])
@login_required
def list_production_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.ProductionID, pr.ProductName, p.HarvestDate, p.ProductionCost, 
               p.Acreage, p.YieldAmount, p.YieldUnit
        FROM productiondata p
        JOIN product pr ON p.ProductID = pr.ProductID
        WHERE p.FarmerID = %s
        ORDER BY p.HarvestDate DESC
    """, (session['user_id'],))
    
    productions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('farmer/production/list.html', productions=productions)

@farmer_routes.route('/farmer/production-data/add', methods=['GET', 'POST'])
@login_required
def add_production_data():
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get list of products for dropdown
        cursor.execute("SELECT ProductID, ProductName FROM product")
        products = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('farmer/production/add.html', products=products)
    
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get form data
            product_id = request.form['product_id']
            harvest_date = request.form['harvest_date']
            production_cost = request.form['production_cost']
            acreage = request.form['acreage']
            yield_amount = request.form['yield_amount']
            yield_unit = request.form['yield_unit']
            
            # Insert production data
            cursor.execute("""
                INSERT INTO productiondata 
                (ProductID, FarmerID, HarvestDate, ProductionCost, 
                 Acreage, YieldAmount, YieldUnit)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (product_id, session['user_id'], harvest_date, 
                 production_cost, acreage, yield_amount, yield_unit))
            
            conn.commit()
            flash('Production data added successfully!', 'success')
            return redirect(url_for('farmer.list_production_data'))
            
        except Exception as e:
            conn.rollback()
            flash(f'Error adding production data: {str(e)}', 'error')
            return redirect(url_for('farmer.add_production_data'))
            
        finally:
            cursor.close()
            conn.close()

@farmer_routes.route('/farmer/production-data/edit/<int:production_id>', methods=['GET', 'POST'])
@login_required
def edit_production_data(production_id):
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get production data
        cursor.execute("""
            SELECT p.ProductionID, p.ProductID, p.HarvestDate, p.ProductionCost, 
                   p.Acreage, p.YieldAmount, p.YieldUnit, pr.ProductName 
            FROM productiondata p
            JOIN product pr ON p.ProductID = pr.ProductID
            WHERE p.ProductionID = %s AND p.FarmerID = %s
        """, (production_id, session['user_id']))
        production = cursor.fetchone()
        
        if not production:
            flash('Production data not found.', 'error')
            return redirect(url_for('farmer.list_production_data'))
        
        # Get list of products for dropdown
        cursor.execute("SELECT ProductID, ProductName FROM product")
        products = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('farmer/production/edit.html', 
                             production=production,
                             products=products)
    
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            product_id = request.form['product_id']
            harvest_date = request.form['harvest_date']
            production_cost = request.form['production_cost']
            acreage = request.form['acreage']
            yield_amount = request.form['yield_amount']
            yield_unit = request.form['yield_unit']
            
            cursor.execute("""
                UPDATE productiondata 
                SET ProductID = %s, HarvestDate = %s, ProductionCost = %s,
                    Acreage = %s, YieldAmount = %s, YieldUnit = %s
                WHERE ProductionID = %s AND FarmerID = %s
            """, (product_id, harvest_date, production_cost,
                 acreage, yield_amount, yield_unit,
                 production_id, session['user_id']))
            
            conn.commit()
            flash('Production data updated successfully!', 'success')
            return redirect(url_for('farmer.list_production_data'))
            
        except Exception as e:
            conn.rollback()
            flash(f'Error updating production data: {str(e)}', 'error')
            return redirect(url_for('farmer.edit_production_data', production_id=production_id))
            
        finally:
            cursor.close()
            conn.close()

@farmer_routes.route('/farmer/request-subsidery', methods=['GET', 'POST'])
def request_subsidery():
    if request.method == 'GET':
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            # Fetch users with Role 'O' (Agricultural Officers)
            cursor.execute("""
                SELECT UserID, CONCAT(FirstName, ' ', LastName) as OfficerName 
                FROM users 
                WHERE Role = 'O'
            """)
            officers = cursor.fetchall()
            
            return render_template('farmer/request-subsidery/subsidery.html', officers=officers)
            
        except Exception as e:
            flash(f'Error loading officers: {str(e)}', 'danger')
            return redirect('farmer/request-subsidery/subsidery.html')
        finally:
            if connection:
                connection.close()
                
    elif request.method == 'POST':
        connection = None
        try:
            subsidy_types = request.form.getlist('subsidyTypes[]')
            quantity = request.form.get('subsideryQuantity')
            officer_id = request.form.get('officerID')
            farmer_id = session['UserID']  # Get farmer ID from session

            
            
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Insert into main subsidery table
            cursor.execute("""
                INSERT INTO farmer_subsidery (FarmerID, OEmployeeID, SubsideryQuantity)
                VALUES (%s, %s, %s)
            """, (farmer_id, officer_id, quantity))

             # Insert subsidy types
            for subsidy_type in subsidy_types:
                cursor.execute("""
                    INSERT INTO farmer_subsidery_type (FarmerID, OEmployeeID, SubsideryType)
                    VALUES (%s, %s, %s)
                """, (farmer_id, officer_id, subsidy_type))
            
            connection.commit()
            flash('Subsidy request submitted successfully!', 'success')
            return redirect('farmer/request-subsidery/subsidery.html')
            
        except Exception as e:
            if connection:
                connection.rollback()
            flash(f'Error submitting request: {str(e)}', 'danger')
            return redirect(farmer/request-subsidery/subsidery.html)
        finally:
            if connection:
                connection.close()