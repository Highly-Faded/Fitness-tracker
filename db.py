import sqlite3

class Database:
    """A context manager for handling database connections."""

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

    def initialize_db(self):
        """Creates the necessary tables if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                weight REAL,
                height REAL,
                activity TEXT,
                bmi REAL,
                calories REAL
            )
        """)

    def save_record(self, name, age, weight, height, activity, bmi, calories):
        """Saves a new health record."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO records (name, age, weight, height, activity, bmi, calories)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, age, weight, height, activity, bmi, calories))
        return cursor.lastrowid

    def fetch_all_records(self):
        """Fetches all health records from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM records ORDER BY id DESC")
        return cursor.fetchall()