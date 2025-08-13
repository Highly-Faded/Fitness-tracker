import sqlite3
import os

class Database:
    """A context manager for handling database connections."""

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def initialize_db(self):
        """Creates the necessary tables if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)

    def insert_record(self, name, email):
        """Inserts a new user record and returns the new user's ID."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Error: Email '{email}' already exists.")
            return None

    def fetch_all_records(self):
        """Fetches all user records from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, email FROM users ORDER BY id")
        return cursor.fetchall()