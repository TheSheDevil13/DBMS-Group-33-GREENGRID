from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash
import pymysql
import sys

officer_routes = Blueprint('officer', __name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  
        database='greengrid'
    )

@officer_routes.route('/agricultural-officer/officer-dashboard')
def officer_dashboard():
    return render_template('agricultural_officer/dashboard/officer-dashboard.html')