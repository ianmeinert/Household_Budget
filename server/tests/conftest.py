import pytest
from src.database.connection import create_tables
from src.utils.db_utils import validate_db_file


@pytest.fixture(scope="session")
def db_file(tmpdir_factory):
    db_file = tmpdir_factory.mktemp("data").join("test_db.sqlite")
    # Validate the db_file using db_utils.dbfile
    validate_db_file(str(db_file))
    create_tables(db_file)
    yield str(db_file)
