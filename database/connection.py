import sqlite3

def get_connection():
    # Return a connection to the SQLite database
    return sqlite3.connect('magazine.db')
