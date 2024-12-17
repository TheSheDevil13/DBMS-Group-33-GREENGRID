from flask import Blueprint, render_template, request, redirect, flash, url_for
import pymysql
import sys
from datetime import datetime

shop_routes = Blueprint('shop', __name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  
        database='greengrid'
    )

@shop_routes.route('/shop/shop-dashboard')
def shop_dashboard():
    try:
        return render_template('retail_shop/dashboard/dashboard.html')
    except Exception as e:
        print(f"Error rendering dashboard: {str(e)}")
        raise

@shop_routes.route('/shop/orders')
def shop_orders():
    return render_template('retail_shop/orders/orders.html')
