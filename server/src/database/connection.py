import sqlite3
from .exceptions import (
    InvalidDatabaseFileError,
)


class DatabaseConnection:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            return self.cursor
        except sqlite3.OperationalError as e:
            raise InvalidDatabaseFileError(f"An error occurred: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def table_exists(self, table_name: str) -> bool:
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return bool(self.cursor.fetchone())

    def create_table(self, create_table_sql: str):
        self.cursor.execute(create_table_sql)


def create_tables(db_file: str):
    with DatabaseConnection(db_file) as cursor:
        tables = {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    disabled INTEGER NOT NULL DEFAULT 0
                )
            """,
            "expenses": """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    estimated_date TEXT NOT NULL,
                    name TEXT NOT NULL,
                    estimated_amount REAL NOT NULL,
                    actual_amount REAL,
                    responsible TEXT NOT NULL,
                    shared INTEGER NOT NULL,
                    disabled INTEGER NOT NULL DEFAULT 0
                )
            """,
            "income": """
                CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    frequency TEXT NOT NULL,
                    disabled INTEGER NOT NULL DEFAULT 0
                )
            """,
        }

        for table_name, create_table_sql in tables.items():
            if not cursor.table_exists(table_name):
                cursor.create_table(create_table_sql)
