from flask import Blueprint, render_template, request, redirect
import pymysql

admin_routes = Blueprint('admin', __name__)

# Connect to the MySQL database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',  # Leave empty if no password
    database='greengrid'
)

cursor = connection.cursor()

# Route for Login page (handles POST)
@admin_routes.route('/admin-dashboard', methods=['GET'])
def admin_dashboard():
    # ... existing code ...
    return render_template('dashboard.html')  # Pass error to template
