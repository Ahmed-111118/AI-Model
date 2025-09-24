import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",      # change if needed
        user="root",           # your MySQL username
        password="ahmed.147",    # your MySQL password
        database="gym_ai"      # the DB name we created
    )
    return conn
