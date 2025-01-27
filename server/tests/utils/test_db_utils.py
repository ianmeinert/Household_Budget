import os
import pytest
from unittest.mock import patch, mock_open
from src.utils.db_utils import validate_db_file, create_db_file


@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open)
@patch("src.utils.db_utils.create_db_file")
def test_validate_db_file_exists(mock_create_db_file, mock_open, mock_exists):
    mock_exists.return_value = True
    db_file = "test_db_file.db"

    validate_db_file(db_file)

    mock_exists.assert_called_once_with(db_file)
    mock_create_db_file.assert_not_called()


@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open)
@patch("src.utils.db_utils.create_db_file")
def test_validate_db_file_not_exists(mock_create_db_file, mock_open, mock_exists):
    mock_exists.return_value = False
    db_file = "test_db_file.db"

    validate_db_file(db_file)

    mock_exists.assert_called_once_with(db_file)
    mock_create_db_file.assert_called_once_with(db_file)


@patch("builtins.open", new_callable=mock_open)
def test_create_db_file(mock_open):
    db_file = "test_db_file.db"

    create_db_file(db_file)

    mock_open.assert_called_once_with(db_file, "w")
