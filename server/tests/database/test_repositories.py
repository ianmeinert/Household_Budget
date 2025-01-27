import unittest
import os
from src.database.connection import DatabaseConnection
from src.database.repositories import (
    UserRepository,
    ExpenseRepository,
    IncomeRepository,
)
from src.database.exceptions import RecordNotFoundError


class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_database.db"
        self.user_repo = UserRepository(self.test_db)
        with DatabaseConnection(self.test_db) as cursor:
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute(
                """
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    disabled INTEGER NOT NULL DEFAULT 0
                )
            """
            )

    def test_add_user(self):
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "secret",
        }
        user = self.user_repo.add_user(user_data)
        self.assertEqual(user[1], "John Doe")

    def test_get_users(self):
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "secret",
        }
        self.user_repo.add_user(user_data)
        users = self.user_repo.get_users()
        self.assertEqual(len(users), 1)

    def test_disable_user(self):
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "secret",
        }
        user = self.user_repo.add_user(user_data)
        self.user_repo.disable_user(user[0])
        with self.assertRaises(RecordNotFoundError):
            self.user_repo.get_user_by_id(user[0])


class TestExpenseRepository(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_database.db"
        self.expense_repo = ExpenseRepository(self.test_db)
        with DatabaseConnection(self.test_db) as cursor:
            cursor.execute("DROP TABLE IF EXISTS expenses")
            cursor.execute(
                """
                CREATE TABLE expenses (
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
            """
            )

    def test_add_expense(self):
        expense_data = {
            "estimated_date": "2023-10-01",
            "name": "Groceries",
            "estimated_amount": 100.0,
            "actual_amount": 90.0,
            "responsible": "John",
            "frequency": "Monthly",
            "shared": 1,
        }
        self.expense_repo.add_expense(expense_data)
        expenses = self.expense_repo.get_expenses()
        self.assertEqual(len(expenses), 1)

    def test_disable_expense(self):
        expense_data = {
            "estimated_date": "2023-10-01",
            "name": "Groceries",
            "estimated_amount": 100.0,
            "actual_amount": 90.0,
            "responsible": "John",
            "frequency": "Monthly",
            "shared": 1,
        }
        self.expense_repo.add_expense(expense_data)
        expense = self.expense_repo.get_expenses()[0]
        self.expense_repo.disable_expense(expense[0])
        with self.assertRaises(RecordNotFoundError):
            self.expense_repo.get_expense_by_id(expense[0])


class TestIncomeRepository(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_database.db"
        self.income_repo = IncomeRepository(self.test_db)
        with DatabaseConnection(self.test_db) as cursor:
            cursor.execute("DROP TABLE IF EXISTS income")
            cursor.execute(
                """
                CREATE TABLE income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    frequency TEXT NOT NULL,
                    bi_weekly_week INTEGER,
                    disabled INTEGER NOT NULL DEFAULT 0
                )
            """
            )

    def test_add_income(self):
        income_data = {"amount": 2000.0, "frequency": "Monthly"}
        self.income_repo.add_income(income_data)
        income = self.income_repo.get_income()
        self.assertEqual(len(income), 1)

    def test_disable_income(self):
        income_data = {"amount": 2000.0, "frequency": "Monthly"}
        self.income_repo.add_income(income_data)
        income = self.income_repo.get_income()[0]
        self.income_repo.disable_income(income[0])
        with self.assertRaises(RecordNotFoundError):
            self.income_repo.get_income_by_id(income[0])


if __name__ == "__main__":
    unittest.main()
