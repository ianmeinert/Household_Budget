# Initialize the database package

from .repositories import ExpenseRepository, IncomeRepository, UserRepository
from .models import Base, engine  # Assuming models.py contains the Base and engine


class RepositorySelector:
    def __init__(self):
        self._repositories = {
            "user": UserRepository(),
            "expense": ExpenseRepository(),
            "income": IncomeRepository(),
        }

    def get_repository(self, name):
        return self._repositories.get(name)


repository_selector = RepositorySelector()
