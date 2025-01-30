import sqlite3
from contextlib import contextmanager

from ..utils import db_utils
from .exceptions import (
    InvalidDatabaseFileError,
)


class DatabaseConnection:
    def __init__(self, db_file: str):
        self.db_file = db_file
        if not db_utils.is_valid_db_file(self.db_file):
            raise InvalidDatabaseFileError(f"Invalid database file: {self.db_file}")
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            return self.cursor
        except sqlite3.OperationalError as e:
            raise InvalidDatabaseFileError(f"An error occurred: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()

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
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return bool(self.cursor.fetchone())

    def create_table(self, create_table_sql: str):
        self.cursor.execute(create_table_sql)


def create_tables(db_file: str):
    db_conn = DatabaseConnection(db_file)
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
            db_conn.create_table(create_table_sql)
