# utils/database.py

import os
import discord
import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self, config, logger):
        self.cfg = config
        self.logger = logger
        self.connection = self.connect_to_db()
        self.cursor = self.connection.cursor()
        logger.info("Database initiated")

    def connect_to_db(self):
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
        if script.endswith(".sql"):
            script_path = os.path.join("./scripts", script)
            try:
                with open(script_path, "r") as file:
                    script = file.read()
            except FileNotFoundError:
                self.logger.error(f"SQL file not found: {script_path}")
                raise

        self.cursor.execute(script, params)

        if script.strip().lower().startswith("select") or script.strip().lower().startswith("with"):
            result = self.cursor.fetchall()
            return result
        else:
            affected_rows = self.cursor.rowcount
            self.connection.commit()
            return affected_rows

    def close(self):
        self.cursor.close()
        self.connection.close()
        self.logger.info("Database connection closed")