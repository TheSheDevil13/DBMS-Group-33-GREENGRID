import pymysql
from pymysql.cursors import DictCursor

def get_db_connection():
    """
    Create and return a database connection with the default configuration.
    Returns:
        pymysql.Connection: A connection object to the database
    """
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  # Leave empty if no password
        database='greengrid',
    )

def get_db_cursor(connection=None):
    """
    Get a database cursor. If no connection is provided, creates a new connection.
    Args:
        connection (pymysql.Connection, optional): Existing database connection
    Returns:
        tuple: (connection, cursor) - The database connection and cursor
    """
    if connection is None:
        connection = get_db_connection()
    cursor = connection.cursor()
    return connection, cursor
