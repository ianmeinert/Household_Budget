import os

import pytest

from src.database.connection import create_tables
from src.utils.db_utils import validate_db_file


@pytest.fixture(scope="function")
def db_file():
    file = "data/budget.sqlite"
    # Validate the db_file using db_utils.dbfile
    validate_db_file(str(file))
    create_tables(file)

    yield str(file)

    # Cleanup code
    try:
        if os.path.exists(file):
            os.remove(file)
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"Error removing the file: {e}")
