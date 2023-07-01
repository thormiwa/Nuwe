import sqlite3

DATABASE = 'nuwe.db'

def create_connection():
    return sqlite3.connect(DATABASE)

def close_connection(conn):
    conn.close()