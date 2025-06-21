import os
import unittest
from unittest.mock import patch, MagicMock, mock_open
from utils.database import Database

class DummyConfig:
    DB_NAME = "test_db"
    DB_USER = "test_user"
    DB_PASS = "test_pass"
    DB_HOST = "localhost"
    DB_PORT = 5432

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Reset singleton so __init__ runs fresh in every test
        Database._instance = None
        if hasattr(Database, '_initialized'):
            delattr(Database, '_initialized')
        self.config = DummyConfig()

    @patch("utils.database.Logger")
    @patch("utils.database.psycopg2.connect")
    def test_connection_and_singleton(self, mock_connect, mock_logger_class):
        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db1 = Database(self.config)
        db2 = Database(self.config)

        # Singleton: both instances are same object
        self.assertIs(db1, db2)

        # Connection and cursor created once
        mock_connect.assert_called_once_with(
            dbname="test_db",
            user="test_user",
            password="test_pass",
            host="localhost",
            port=5432,
        )
        mock_conn.cursor.assert_called_once()
        mock_logger.info.assert_any_call("Database initiated")
        mock_logger.info.assert_any_call("Successfully connected to the database")

    @patch("builtins.open", new_callable=mock_open, read_data="UPDATE something SET val=1;")
    @patch("utils.database.Logger")
    @patch("utils.database.psycopg2.connect")
    def test_run_script_sql_file(self, mock_connect, mock_logger_class, mock_file):
        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = Database(self.config)

        mock_cursor.rowcount = 1
        result = db.run_script("test.sql")

        mock_file.assert_called_once_with(os.path.join("./scripts", "test.sql"), "r")
        mock_cursor.execute.assert_called_once_with("UPDATE something SET val=1;", None)
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, 1)

    @patch("utils.database.Logger")
    @patch("utils.database.psycopg2.connect")
    def test_run_script_select_query(self, mock_connect, mock_logger_class):
        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = Database(self.config)

        expected_rows = [("row1",), ("row2",)]
        mock_cursor.fetchall.return_value = expected_rows

        sql = "SELECT * FROM users WHERE id = %s"
        params = (42,)

        result = db.run_script(sql, params)

        mock_cursor.execute.assert_called_once_with(sql, params)
        mock_cursor.fetchall.assert_called_once()
        self.assertEqual(result, expected_rows)
        # No commit expected for SELECT
        mock_conn.commit.assert_not_called()

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("utils.database.Logger")
    @patch("utils.database.psycopg2.connect")
    def test_run_script_file_not_found(self, mock_connect, mock_logger_class, mock_open):
        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = Database(self.config)

        with self.assertRaises(FileNotFoundError):
            db.run_script("nonexistent.sql")

        expected_path = os.path.join("./scripts", "nonexistent.sql")
        mock_logger.error.assert_called_with(f"SQL file not found: {expected_path}")

    @patch("utils.database.Logger")
    @patch("utils.database.psycopg2.connect")
    def test_close_closes_cursor_and_connection(self, mock_connect, mock_logger_class):
        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = Database(self.config)

        db.close()

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_logger.info.assert_called_with("Database connection closed")

if __name__ == "__main__":
    unittest.main()
