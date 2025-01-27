import unittest
import pytest
from src.utils.db_utils import validate_db_file
from src.database.connection import DatabaseConnection, create_tables
from src.database.exceptions import InvalidDatabaseFileError


class TestDatabaseConnection(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def assign_test_db(self, tmpdir_factory):
        self.test_db = tmpdir_factory.mktemp("data").join("test_db.sqlite")
        validate_db_file(str(self.test_db))

    def setUp(self):
        with DatabaseConnection(self.test_db) as cursor:
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("DROP TABLE IF EXISTS expenses")
            cursor.execute("DROP TABLE IF EXISTS income")

    def test_database_connection(self):
        with DatabaseConnection(self.test_db) as cursor:
            cursor.execute("SELECT 1")
            self.assertEqual(cursor.fetchone()[0], 1)

    def test_table_exists(self):
        db_conn = DatabaseConnection(self.test_db)
        self.assertFalse(db_conn.table_exists("users"))
        db_conn.create_table(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """
        )
        self.assertTrue(db_conn.table_exists("users"))

    def test_create_tables(self):
        create_tables(self.test_db)
        db_conn = DatabaseConnection(self.test_db)
        self.assertTrue(db_conn.table_exists("users"))
        self.assertTrue(db_conn.table_exists("expenses"))
        self.assertTrue(db_conn.table_exists("income"))

    def test_invalid_database_file(self):
        with self.assertRaises(InvalidDatabaseFileError):
            db_conn = DatabaseConnection("invalid_path/test.db")


if __name__ == "__main__":
    unittest.main()
