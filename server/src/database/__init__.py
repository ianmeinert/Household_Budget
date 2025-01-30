# Initialize the database package

from ..utils.db_utils import validate_db_file
from .connection import create_tables
from .factory import RepositoryFactory
import os
from dotenv import load_dotenv


class RepositorySelector:

    def __init__(self, dbfile):
        validate_db_file(dbfile)
        # check if the sqlite file is empty
        if os.stat(dbfile).st_size == 0:
            # if its empty, populate the tables
            create_tables(dbfile)

        self._repository_factory: RepositoryFactory = RepositoryFactory(dbfile)
        self._repositories = {
            "user": self._repository_factory.get_user_repository(),
            "expense": self._repository_factory.get_expense_repository(),
            "income": self._repository_factory.get_income_repository(),
        }

    def get_repository(self, name):
        return self._repositories.get(name)


load_dotenv()
dbfile = os.getenv("DBFILE")

repository_selector = RepositorySelector(dbfile)
