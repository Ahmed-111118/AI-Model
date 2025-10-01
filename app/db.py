import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """
    Create and return a MySQL database connection.
    Raises a clear error if connection fails.
    """

    try:
        conn = mysql.connector.connect(
            host="localhost",       # ✅ Database host
            user="root",            # ✅ Your MySQL username
            password="ahmed.147",   # ✅ Your MySQL password
            database="gym_ai"       # ✅ Your database name
        )

        if conn.is_connected():
            print("✅ Database connection successful!")
            return conn
        else:
            raise ConnectionError("❌ Failed to connect to MySQL database.")

    except Error as e:
        print("❌ MySQL connection error:", e)
        raise e
