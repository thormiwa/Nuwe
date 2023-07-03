import re, os
from db import create_connection, close_connection
from datetime import datetime
import config

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    else:
        return False
    
def connect_to_db(query, insert=False, fetchall=False, params=None):

    if not os.path.exists(config.DATABASE_NAME):
        create_database()

    conn, db_cursor = start_connection()
    
    if params is not None:
        db_cursor.execute(query, params)
    else:
        db_cursor.execute(query)
    
    if fetchall:
        result = db_cursor.fetchall()
    else:
        result = db_cursor.fetchone()

    end_connection(conn, db_cursor)
    if not insert:
        return result

def create_database():
    conn, db_cursor = start_connection()
    
    # Create tables and perform other initializations
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            connection_date TEXT NOT NULL,
            http_verb TEXT NOT NULL,
            endpoint TEXT NOT NULL
        )
    ''')
    
    end_connection(conn, db_cursor) 

def start_connection():
    conn = create_connection()
    db_cursor = conn.cursor()
    return conn, db_cursor

def end_connection(conn, db_cursor):
    conn.commit()
    db_cursor.close()
    close_connection(conn)
        
def log_connection(request):
    ip = request.remote_addr 
    date = datetime.now().strftime("%b %d, %Y")  
    http_verb = request.method 
    endpoint = request.path 

    log_query = 'INSERT INTO connections (ip, connection_date, http_verb, endpoint) VALUES (?, ?, ?, ?)'
    params = (ip, date, http_verb, endpoint)
    connect_to_db(log_query, insert=True, params=params)