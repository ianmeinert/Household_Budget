# global errors
class DatabaseError(Exception):
    """Exception raised for errors that occur during database operations."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(DatabaseError):
    """Exception raised when a user is not found in the database."""

    def __init__(self, user_id: int):
        self.message = f"User with ID {user_id} not found."
        super().__init__(self.message)


class ExpenseNotFoundError(DatabaseError):
    """Exception raised when an expense is not found in the database."""

    def __init__(self, expense_id: int):
        self.message = f"Expense with ID {expense_id} not found."
        super().__init__(self.message)


class IncomeNotFoundError(DatabaseError):
    """Exception raised when an income record is not found in the database."""

    def __init__(self, income_id: int):
        self.message = f"Income record with ID {income_id} not found."
        super().__init__(self.message)


class DuplicateUserError(DatabaseError):
    """Exception raised when attempting to add a duplicate user."""

    def __init__(self, email: str):
        self.message = f"User with email {email} already exists."
        super().__init__(self.message)


class InvalidDataError(DatabaseError):
    """Exception raised when invalid data is provided."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RecordNotFoundError(DatabaseError):
    """Exception raised when a record is not found in the database."""

    def __init__(self, record_type: str = "", record_id: int = 0):
        self.message = f"{record_type} with ID {record_id} not found."
        super().__init__(self.message)


class InvalidDatabaseFileError(DatabaseError):
    """Exception raised for invalid database file errors."""

    def __init__(self, message="Invalid database file."):
        self.message = message
        super().__init__(self.message)
