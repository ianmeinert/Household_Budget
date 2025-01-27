import unittest
from src.database.factory import RepositoryFactory
from src.database.repositories import (
    UserRepository,
    ExpenseRepository,
    IncomeRepository,
)


class TestRepositoryFactory(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_database.db"
        self.factory = RepositoryFactory(self.test_db)

    def test_get_user_repository(self):
        user_repo = self.factory.get_user_repository()
        self.assertIsInstance(user_repo, UserRepository)

    def test_get_expense_repository(self):
        expense_repo = self.factory.get_expense_repository()
        self.assertIsInstance(expense_repo, ExpenseRepository)

    def test_get_income_repository(self):
        income_repo = self.factory.get_income_repository()
        self.assertIsInstance(income_repo, IncomeRepository)


if __name__ == "__main__":
    unittest.main()
