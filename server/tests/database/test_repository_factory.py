import unittest
import pytest
from src.database.factory import RepositoryFactory
from src.database.repositories import (
    UserRepository,
    ExpenseRepository,
    IncomeRepository,
)
from src.utils.db_utils import validate_db_file


class TestRepositoryFactory(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def assign_test_db(self, tmpdir_factory):
        self.test_db = tmpdir_factory.mktemp("data").join("test_db.sqlite")
        validate_db_file(str(self.test_db))

    def setUp(self):
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
