import sqlite3

from ..utils import db_utils
from .exceptions import (
    InvalidDatabaseFileError,
)


class DatabaseConnection:
    def __init__(self, db_file: str):
        if not db_utils.is_valid_db_file(db_file):
            raise InvalidDatabaseFileError(f"Invalid database file: {db_file}")
        else:
            self.db_file = db_file
            self.conn = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            return self
        except sqlite3.OperationalError as e:
            raise InvalidDatabaseFileError(f"An error occurred: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def execute(self, query, params=None):
        if params is None:
            params = []
        self.validate_sql(query)
        with self as cursor:
            cursor.execute(query, params)

    def executemany(self, query, params_list):
        self.validate_sql(query)
        with self as cursor:
            cursor.executemany(query, params_list)

    def fetchall(self, query, params=None):
        if params is None:
            params = []
        self.validate_sql(query)
        with self as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetchone(self, query, params=None):
        if params is None:
            params = []
        self.validate_sql(query)
        with self as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    @staticmethod
    def validate_sql(query):
        allowed_statements = ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"]
        if not any(
            query.strip().upper().startswith(stmt) for stmt in allowed_statements
        ):
            raise ValueError("Invalid SQL statement")

    def table_exists(self, table_name: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return cursor.fetchone() is not None

    def create_table(self, create_table_sql: str):
        cursor = self.connection.cursor()
        cursor.execute(create_table_sql)


def create_tables(db_file: str):
    with DatabaseConnection(db_file) as db_conn:
        tables = {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    private_key TEXT NOT NULL,
                    cyphertext TEXT NOT NULL,
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
                    frequency TEXT NOT NULL,
                    shared INTEGER NOT NULL,
                    disabled INTEGER NOT NULL DEFAULT 0
                )
            """,
            "income": """
                CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    frequency TEXT NOT NULL,
                    bi_weekly_week INTEGER,
                    disabled INTEGER NOT NULL DEFAULT 0
                )
            """,
        }

        for table_name, create_table_sql in tables.items():
            if not db_conn.table_exists(table_name):
                cursor = db_conn.connection.cursor()
                cursor.execute(create_table_sql)
