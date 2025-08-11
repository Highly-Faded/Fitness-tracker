import sqlite3
from sqlite3 import Error

class Database:
    """A class to manage SQLite database operations."""

    def __init__(self, db_file):
        """
        Initialize the Database object and connect to the SQLite database.

        :param db_file: The path to the database file.
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            print(f"Successfully connected to SQLite database: {db_file}")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context and close the database connection."""
        self.close_connection()


    def initialize_db(self):
        """
        Initializes the database by creating the necessary tables if they don't exist.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
        """
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'users' created or already exists.")
        except Error as e:
            print(f"Error creating table: {e}")

    def insert_record(self, name, email):
        """
        Insert a new record into the users table.

        :param name: The name of the user.
        :param email: The email of the user.
        :return: The ID of the newly inserted row, or None on failure.
        """
        sql = ''' INSERT INTO users(name, email)
                  VALUES(?, ?) '''
        try:
            self.cursor.execute(sql, (name, email))
            self.conn.commit()
            print(f"Record inserted for user: {name}")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Error: Email '{email}' already exists.")
            return None
        except Error as e:
            print(f"Error inserting record: {e}")
            return None

    def fetch_all_records(self):
        """
        Query all rows in the users table.

        :return: A list of all records as tuples.
        """
        try:
            self.cursor.execute("SELECT * FROM users")
            rows = self.cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error fetching records: {e}")
            return []

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    # Define the database file name
    db_file = "mydatabase.db"

    # Create a database connection
    db = Database(db_file)

    # Check if the connection was successful before proceeding
    if db.conn:
        # Initialize the database (create the 'users' table)
        db.initialize_db()

        # --- Insert some sample records ---
        print("\n--- Inserting Records ---")
        db.insert_record("Alice", "alice@example.com")
        db.insert_record("Bob", "bob@example.com")
        db.insert_record("Charlie", "charlie@example.com")
        # This insert will fail due to the UNIQUE constraint on the email
        db.insert_record("Another Alice", "alice@example.com")

        # --- Fetch and display all records ---
        print("\n--- Fetching All Records ---")
        all_users = db.fetch_all_records()
        for user in all_users:
            print(user)

        # --- Close the connection ---
        db.close_connection()
