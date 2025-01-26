import sqlite3
from typing import Any, List

from .connection import DatabaseConnection
from .exceptions import (
    DatabaseError,
    UserNotFoundError,
    ExpenseNotFoundError,
    IncomeNotFoundError,
    InvalidDataError,
    DuplicateUserError,
    RecordNotFoundError,
)


class Repository:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def execute_query(self, query: str, params: List[Any] = []):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise DatabaseError(f"An error occurred: {e}")

    def execute_non_query(self, query: str, params: List[Any] = []):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                cursor.execute(query, params)
        except sqlite3.Error as e:
            raise DatabaseError(f"An error occurred: {e}")


class UserRepository(Repository):
    def get_users(self):
        users = self.execute_query("SELECT * FROM users WHERE disabled = 0")
        if not users:
            raise UserNotFoundError(0)  # Assuming 0 as a placeholder
        return users

    def add_user(self, user_data: dict):
        existing_user = self.execute_query(
            "SELECT * FROM users WHERE email = ? AND disabled = 0", [user_data["email"]]
        )
        if existing_user:
            raise DuplicateUserError(user_data["email"])
        self.execute_non_query(
            "INSERT INTO users (name, email, disabled) VALUES (?, ?, 0)",
            [user_data["name"], user_data["email"]],
        )

    def disable_user(self, user_id: int):
        self.execute_non_query("UPDATE users SET disabled = 1 WHERE id = ?", [user_id])

    def get_user_by_id(self, user_id: int):
        user = self.execute_query(
            "SELECT * FROM users WHERE id = ? AND disabled = 0", [user_id]
        )
        if not user:
            raise RecordNotFoundError(f"User with id {user_id} not found.")
        return user


class ExpenseRepository(Repository):
    def get_expenses(self):
        expenses = self.execute_query("SELECT * FROM expenses WHERE disabled = 0")
        if not expenses:
            raise ExpenseNotFoundError(0)  # Assuming 0 as a placeholder
        return expenses

    def add_expense(self, expense_data: dict):
        if not all(
            key in expense_data
            for key in [
                "estimated_date",
                "name",
                "estimated_amount",
                "actual_amount",
                "responsible",
                "shared",
            ]
        ):
            raise InvalidDataError("Missing required expense data fields.")
        self.execute_non_query(
            """INSERT INTO expenses (estimated_date, name, estimated_amount, actual_amount, responsible, shared, disabled) 
               VALUES (?, ?, ?, ?, ?, ?, 0)""",
            [
                expense_data["estimated_date"],
                expense_data["name"],
                expense_data["estimated_amount"],
                expense_data["actual_amount"],
                expense_data["responsible"],
                expense_data["shared"],
            ],
        )

    def disable_expense(self, expense_id: int):
        self.execute_non_query(
            "UPDATE expenses SET disabled = 1 WHERE id = ?", [expense_id]
        )

    def get_expense_by_id(self, expense_id: int):
        expense = self.execute_query(
            "SELECT * FROM expenses WHERE id = ? AND disabled = 0", [expense_id]
        )
        if not expense:
            raise RecordNotFoundError(f"Expense with id {expense_id} not found.")
        return expense


class IncomeRepository(Repository):
    def get_expenses(self):
        income = self.execute_query("SELECT * FROM income WHERE disabled = 0")
        if not income:
            raise IncomeNotFoundError(0)  # Assuming 0 as a placeholder
        return income

    def add_expense(self, expense_data: dict):
        if not all(key in expense_data for key in ["amount", "frequency"]):
            raise InvalidDataError("Missing required income data fields.")
        self.execute_non_query(
            "INSERT INTO income (amount, frequency, disabled) VALUES (?, ?, 0)",
            [expense_data["amount"], expense_data["frequency"]],
        )

    def disable_expense(self, income_id: int):
        self.execute_non_query(
            "UPDATE income SET disabled = 1 WHERE id = ?", [income_id]
        )

    def get_income_by_id(self, income_id: int):
        income = self.execute_query(
            "SELECT * FROM income WHERE id = ? AND disabled = 0", [income_id]
        )
        if not income:
            raise RecordNotFoundError(f"Income with id {income_id} not found.")
        return income
