import os
import psycopg2
from utils.logger import Logger

class Database:
    """
    Singleton PostgreSQL Database utility for connection and query execution.

    Usage:
        from utils.database import Database
        db = Database(config, logger)
        result = db.run_script("SELECT * FROM users WHERE id = %s", (user_id,))
        db.close()
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config):
        """
        Initialize DB connection and cursor (only once).

        Args:
            config: Config object with DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT.
            logger: Logger instance for logging.
        """
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.logger = Logger()
        self.cfg = config
        self.connection = self.connect_to_db()
        self.cursor = self.connection.cursor()
        self.logger.info("Database initiated")
        self._initialized = True

    def connect_to_db(self):
        """Connect to PostgreSQL and return connection."""
        try:
            conn = psycopg2.connect(
                dbname=self.cfg.DB_NAME,
                user=self.cfg.DB_USER,
                password=self.cfg.DB_PASS,
                host=self.cfg.DB_HOST,
                port=self.cfg.DB_PORT
            )
            self.logger.info("Successfully connected to the database")
            return conn
        except Exception as e:
            self.logger.error(f"Database connection error: {e}")
            raise

    def run_script(self, script, params=None):
        """
        Execute SQL command or script file and return results or affected rows.
        Retry connection once if a connection-related error occurs.

        Args:
            script (str): SQL query or filename ending with '.sql'.
            params (tuple/dict, optional): Parameters for query placeholders.

        Returns:
            list: Query results for SELECT/ WITH.
            int: Number of affected rows for others.
            False: If execution fails after retry.
        """
        if script.endswith(".sql"):
            script_path = os.path.join("./scripts", script)
            try:
                with open(script_path, "r") as file:
                    script = file.read()
            except FileNotFoundError:
                self.logger.error(f"SQL file not found: {script_path}")
                raise

        def execute_query():
            self.cursor.execute(script, params)
            if script.strip().lower().startswith(("select", "with")):
                return self.cursor.fetchall()
            else:
                affected = self.cursor.rowcount
                self.connection.commit()
                return affected

        try:
            return execute_query()
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            # These errors typically indicate connection problems
            self.logger.warning(f"Database operation failed, retrying once: {e}")
            try:
                self.connection.close()
            except Exception:
                pass
            try:
                self.connection = self.connect_to_db()
                self.cursor = self.connection.cursor()
                return execute_query()
            except Exception as e2:
                self.logger.error(f"Retry failed: {e2}")
                return False
        except Exception as e:
            self.logger.error(f"Database operation error: {e}")
            return False

    def close(self):
        """Close cursor and DB connection."""
        self.cursor.close()
        self.connection.close()
        self.logger.info("Database connection closed")
