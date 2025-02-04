import os


def is_valid_db_file(db_file):
    return os.path.exists(db_file)


def validate_db_file(db_file):
    if not os.path.exists(db_file):
        create_db_file(db_file)


def create_db_file(db_file):
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    open(db_file, "a").close()
