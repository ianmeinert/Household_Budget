# Initialize the database package

from .repositories import ExpenseRepository, IncomeRepository, UserRepository
import os
from dotenv import load_dotenv


class RepositorySelector:

    def __init__(self, dbfile):
        self._repositories = {
            "user": UserRepository(dbfile),
            "expense": ExpenseRepository(dbfile),
            "income": IncomeRepository(dbfile),
        }

    def get_repository(self, name):
        return self._repositories.get(name)


load_dotenv()
dbfile = os.getenv("DBFILE")

repository_selector = RepositorySelector(dbfile)
