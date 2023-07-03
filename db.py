import sqlite3
import config


def create_connection():
    return sqlite3.connect(config.DATABASE_NAME)

def close_connection(conn):
    conn.close()