from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from werkzeug.security import generate_password_hash
import pymysql
import sys
from datetime import datetime

farmer_routes = Blueprint('farmer', __name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  
        database='greengrid'
    )

@farmer_routes.route('/farmer/farmer-dashboard')
def farmer_dashboard():
    print("Debug: Accessing farmer dashboard route")  # Debug print
    try:
        return render_template('farmer/dashboard/farmer-dashboard.html')
    except Exception as e:
        print(f"Debug: Error rendering farmer dashboard - {str(e)}")  # Debug print
        raise

@farmer_routes.route('/farmer/production-data')
def production_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Fetch production data with farmer and product names, plus calculated expiration date
        cursor.execute("""
            SELECT pd.*,
                   CONCAT(u.FirstName, ' ', u.LastName) as FarmerName,
                   p.ProductName,
                   DATE_ADD(pd.HarvestDate, INTERVAL pd.ShelfLife DAY) as ExpirationDate
            FROM productiondata pd
            LEFT JOIN users u ON pd.FarmerID = u.UserID
            LEFT JOIN product p ON pd.ProductID = p.ProductID
            WHERE u.Role = 'F'
            ORDER BY pd.ProductionID DESC
        """)
        productions = cursor.fetchall()
        
        # Fetch farmers for dropdown
        cursor.execute("""
            SELECT UserID as FarmerID, 
                   CONCAT(FirstName, ' ', LastName) as FarmerName 
            FROM users 
            WHERE Role = 'F' 
            ORDER BY FirstName, LastName
        """)
        farmers = cursor.fetchall()
        
        # Fetch products for dropdown
        cursor.execute("SELECT ProductID, ProductName FROM product ORDER BY ProductName")
        products = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('farmer/production-data/production-data.html', 
                             productions=productions,
                             farmers=farmers,
                             products=products)
    except Exception as e:
        print(f"Error fetching production data: {str(e)}")
        flash('Error fetching production data', 'error')
        return redirect(url_for('farmer_routes.farmer_dashboard'))

@farmer_routes.route('/farmer/add-production', methods=['POST'])
def add_production():
    if request.method == 'POST':
        connection = None
        try:
            # Print form data for debugging
            print("\nDebug: Form data received:")
            for key, value in request.form.items():
                print(f"{key}: {value}")

            farmer_id = request.form['farmerID']
            product_id = request.form.get('productID')  # This can be None
            harvest_date = request.form['harvestDate']
            production_cost = request.form['productionCost']
            shelf_life = request.form['shelfLife']
            acreage = request.form['acreage']
            yield_rate = request.form['yieldRate']

            print("\nDebug: Parsed values:")
            print(f"farmer_id: {farmer_id}, type: {type(farmer_id)}")
            print(f"product_id: {product_id}, type: {type(product_id)}")
            print(f"harvest_date: {harvest_date}, type: {type(harvest_date)}")
            print(f"production_cost: {production_cost}, type: {type(production_cost)}")
            print(f"shelf_life: {shelf_life}, type: {type(shelf_life)}")
            print(f"acreage: {acreage}, type: {type(acreage)}")
            print(f"yield_rate: {yield_rate}, type: {type(yield_rate)}")

            connection = get_db_connection()
            cursor = connection.cursor()

            # First verify if the farmer exists
            cursor.execute("SELECT UserID FROM users WHERE UserID = %s AND Role = 'F'", (farmer_id,))
            if not cursor.fetchone():
                raise ValueError(f"Invalid farmer ID: {farmer_id}")

            # If product_id is provided, verify it exists
            if product_id:
                cursor.execute("SELECT ProductID FROM product WHERE ProductID = %s", (product_id,))
                if not cursor.fetchone():
                    raise ValueError(f"Invalid product ID: {product_id}")

            # First, let's modify the foreign key constraint
            try:
                print("\nDebug: Dropping old foreign key constraint...")
                cursor.execute("""
                    ALTER TABLE productiondata 
                    DROP FOREIGN KEY productiondata_ibfk_2
                """)
                connection.commit()
                
                print("Debug: Adding new foreign key constraint...")
                cursor.execute("""
                    ALTER TABLE productiondata 
                    ADD CONSTRAINT productiondata_farmer_fk 
                    FOREIGN KEY (FarmerID) 
                    REFERENCES users(UserID) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
                """)
                connection.commit()
            except Exception as e:
                print(f"Note: Foreign key modification failed (this is okay if already updated): {str(e)}")

            # Now insert the production data
            query = """
            INSERT INTO productiondata 
            (HarvestDate, ProductionCost, ShelfLife, Acreage, YieldRate, FarmerID, ProductID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            print("\nDebug: Executing query:", query)
            print("Debug: Values:", (harvest_date, production_cost, shelf_life, 
                                   acreage, yield_rate, farmer_id, product_id))
            
            cursor.execute(query, (harvest_date, production_cost, shelf_life, 
                                 acreage, yield_rate, farmer_id, product_id))
            connection.commit()
            print("Debug: Data inserted successfully")

            cursor.close()
            connection.close()

            flash('Production record added successfully', 'success')
            return redirect('/farmer/production-data')
        except Exception as e:
            print("\nError adding production record:")
            print(f"Error type: {type(e)}")
            print(f"Error message: {str(e)}")
            import traceback
            print(f"Traceback:\n{traceback.format_exc()}")
            flash('Error adding production record: ' + str(e), 'error')
            if connection:
                connection.close()
            return redirect('/farmer/production-data')

@farmer_routes.route('/farmer/delete-production/<int:production_id>', methods=['DELETE'])
def delete_production(production_id):
    print("Debug: Accessing delete production route")  # Debug print
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "DELETE FROM productiondata WHERE ProductionID = %s"
        cursor.execute(query, (production_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting production record: {e}")
        return jsonify({'success': False, 'error': str(e)})