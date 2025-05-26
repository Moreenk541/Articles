import sqlite3

def get_connection():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row # This enables column access by name
    return conn

def get_cursor():
    conn = get_connection()
    return conn, conn.cursor()
