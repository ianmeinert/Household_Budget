from .database.connection import create_tables
from .utils.db_utils import validate_db_file


def main():
    db_file = "path/to/your/database.db"
    validate_db_file()
    create_tables(db_file)
    # ...existing code...


if __name__ == "__main__":
    main()
