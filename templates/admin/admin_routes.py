from flask import Blueprint, render_template, request, redirect
import pymysql

admin_routes = Blueprint('admin', __name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  
        database='greengrid'
    )

@admin_routes.route('/admin/admin-dashboard')
def admin_dashboard():
    # Test data without database connection
    test_pending_users = [
        {
            'UserID': 1,
            'FirstName': 'Test',
            'LastName': 'User',
            'Username': 'testuser',
            'Email': 'test@example.com',
            'Role': 'F',
            'Status': 'pending'
        },
        {
            'UserID': 2,
            'FirstName': 'John',
            'LastName': 'Doe',
            'Username': 'johndoe',
            'Email': 'john@example.com',
            'Role': 'W',
            'Status': 'pending'
        }
    ]
    print("Sending test data to template:", test_pending_users)
    return render_template('admin/admin-dashboard.html', pending_users=test_pending_users)

