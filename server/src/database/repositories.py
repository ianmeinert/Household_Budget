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
from .schemas import User


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

    def fetch_one(self, query: str, params: List[Any] = []):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except sqlite3.Error as e:
            raise DatabaseError(f"An error occurred: {e}")

    def execute_non_query(self, query: str, params: List[Any] = []):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                cursor.execute(query, params)
        except sqlite3.Error as e:
            raise DatabaseError(f"An error occurred: {e}")


class UserRepository(Repository):
    def get_users(self) -> List[User]:
        users: List[User] = self.execute_query("SELECT * FROM users WHERE disabled = 0")
        if not users:
            raise UserNotFoundError(0)  # Assuming 0 as a placeholder
        return [
            User(
                id=user[0],
                username=user[1],
                first_name=user[2],
                last_name=user[3],
                email=user[4],
                password=str(),
                encrypted_password=user[5],
                private_key=user[6],
                cyphertext=user[7],
            )
            for user in users
        ]

    def add_user(self, user_data: dict):
        try:
            required_fields = [
                "username",
                "first_name",
                "last_name",
                "email",
                "password",
                "private_key",
            ]
            if not all(key in user_data for key in required_fields):
                raise InvalidDataError("Missing required user data fields.")
            existing_user = self.get_user_by_username(user_data["username"])
            if existing_user:
                raise DuplicateUserError(user_data["username"])
        except RecordNotFoundError:
            user: User = User(**user_data)
            user.encrypt_password()
            self.execute_non_query(
                "INSERT INTO users (username, first_name, last_name, email, password, private_key, cyphertext, disabled) VALUES (?, ?, ?, ?, ?, ?, ?, 0)",
                [
                    user.username,
                    user.first_name,
                    user.last_name,
                    user.email,
                    user.encrypted_password,
                    user.private_key,
                    user.cyphertext,
                ],
            )
        return self.get_user_by_username(user_data["username"])

    def disable_user(self, user_id: int):
        self.execute_non_query("UPDATE users SET disabled = 1 WHERE id = ?", [user_id])

    def get_user_by_id(self, user_id: int) -> User:
        user = self.execute_query(
            "SELECT id, username, first_name, last_name, email, password, private_key, cyphertext FROM users WHERE id = ? AND disabled = 0",
            [user_id],
        )
        if not user:
            raise RecordNotFoundError(record_type="User", record_id=user_id)
        user_data = user[0]
        return User(
            id=user_data[0],
            username=user_data[1],
            first_name=user_data[2],
            last_name=user_data[3],
            email=user_data[4],
            encrypted_password=user_data[5],
            private_key=user_data[6],
            cyphertext=user_data[7],
        )

    def get_user_by_name(self, name: str) -> User:
        user = self.execute_query(
            "SELECT id, username, first_name, last_name, email, password, private_key, cyphertext FROM users WHERE username = ? AND disabled = 0",
            [name],
        )
        if not user:
            raise RecordNotFoundError(record_type="User", record_id=0)
        user_data = user[0]
        return User(
            id=user_data[0],
            username=user_data[1],
            first_name=user_data[2],
            last_name=user_data[3],
            email=user_data[4],
            password=str(),
            encrypted_password=user_data[5],
            private_key=user_data[6],
            cyphertext=user_data[7],
        )

    def get_user_by_username(self, username: str) -> User:
        user_data = self.fetch_one(
            "SELECT id, username, first_name, last_name, email, password, private_key, cyphertext FROM users WHERE username = ? AND disabled = 0 LIMIT 1",
            [username],
        )
        if not user_data:
            raise RecordNotFoundError(record_type="User", record_id=0)

        user: User = User(
            id=user_data[0],
            username=user_data[1],
            first_name=user_data[2],
            last_name=user_data[3],
            email=user_data[4],
            password=str(),
            encrypted_password=user_data[5],
            private_key=user_data[6],
            cyphertext=user_data[7],
        )

        return user

    def get_user_credentials_by_id(self, id: int) -> User:
        user = self.execute_query(
            "SELECT id, username, first_name, last_name, email, password, private_key, cyphertext FROM users WHERE id = ? AND disabled = 0",
            [id],
        )
        if not user:
            raise RecordNotFoundError(record_type="User", record_id=id)
        user_data = user[0]
        return User(
            id=user_data[0],
            username=user_data[1],
            first_name=user_data[2],
            last_name=user_data[3],
            email=user_data[4],
            encrypted_password=user_data[5],
            private_key=user_data[6],
            cyphertext=user_data[7],
        )


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
                "frequency",
                "shared",
            ]
        ):
            raise InvalidDataError("Missing required expense data fields.")
        self.execute_non_query(
            """INSERT INTO expenses (estimated_date, name, estimated_amount, actual_amount, responsible, frequency, shared, disabled) 
               VALUES (?, ?, ?, ?, ?, ?, ?, 0)""",
            [
                expense_data["estimated_date"],
                expense_data["name"],
                expense_data["estimated_amount"],
                expense_data["actual_amount"],
                expense_data["responsible"],
                expense_data["frequency"],
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
            raise RecordNotFoundError(record_type="Expenses", record_id=expense_id)
        return expense


class IncomeRepository(Repository):
    VALID_FREQUENCIES = ["Bi-weekly", "Weekly", "Monthly", "Semi-Monthly", "Daily"]

    def validate_frequency(self, frequency: str):
        if frequency not in self.VALID_FREQUENCIES:
            raise InvalidDataError(f"Invalid frequency: {frequency}")

    def get_income(self):
        income = self.execute_query("SELECT * FROM income WHERE disabled = 0")
        if not income:
            raise IncomeNotFoundError(0)  # Assuming 0 as a placeholder
        return income

    def add_income(self, income_data: dict):
        if not all(key in income_data for key in ["amount", "frequency"]):
            raise InvalidDataError("Missing required income data fields.")
        self.validate_frequency(income_data["frequency"])
        bi_weekly_week = income_data.get("bi_weekly_week", None)
        if income_data["frequency"] == "Bi-weekly" and bi_weekly_week not in [1, 2]:
            raise InvalidDataError(
                "Bi-weekly income must specify 'bi_weekly_week' as 1 or 2."
            )
        self.execute_non_query(
            "INSERT INTO income (amount, frequency, bi_weekly_week, disabled) VALUES (?, ?, ?, 0)",
            [income_data["amount"], income_data["frequency"], bi_weekly_week],
        )

    def disable_income(self, income_id: int):
        self.execute_non_query(
            "UPDATE income SET disabled = 1 WHERE id = ?", [income_id]
        )

    def get_income_by_id(self, income_id: int):
        income = self.execute_query(
            "SELECT * FROM income WHERE id = ? AND disabled = 0", [income_id]
        )
        if not income:
            raise RecordNotFoundError(record_type="Income", record_id=income_id)
        return income
