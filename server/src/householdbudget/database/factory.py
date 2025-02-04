from .repositories import UserRepository, ExpenseRepository, IncomeRepository


class RepositoryFactory:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def get_user_repository(self):
        return UserRepository(self.db_file)

    def get_expense_repository(self):
        return ExpenseRepository(self.db_file)

    def get_income_repository(self):
        return IncomeRepository(self.db_file)
