import os
import sqlite3
from sqlite3 import Connection
from app.core.logger import get_logger

logger = get_logger(__name__)

DATABASE_NAME = os.environ.get("FAIRRANK_DB", "fairrank.db")


def get_connection() -> Connection:
    logger.debug("Opening DB connection to %s", DATABASE_NAME)
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def execute_script(script: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.executescript(script)
        conn.commit()
        logger.info("Executed DB script successfully")
    except Exception:
        logger.exception("Failed to execute DB script")
        raise
    finally:
        try:
            conn.close()
        except Exception:
            pass
# app/core/database.py

import os
import sqlite3
from sqlite3 import Connection
from app.core.logger import get_logger

logger = get_logger(__name__)

# Allow DB override via env for testing
DATABASE_NAME = os.environ.get("FAIRRANK_DB", "fairrank.db")


def get_connection() -> Connection:
    """Return an SQLite connection configured with row factory and FK support.

    Raises sqlite3.Error on failure which should be logged by callers.
    """
    logger.debug("Opening DB connection to %s", DATABASE_NAME)
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def execute_script(script: str):
    """Execute a multi-statement SQL script (used for schema initialization).

    Any errors are logged and re-raised to make failures visible.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executescript(script)
        conn.commit()
        logger.info("Executed DB script successfully")
    except Exception:
        logger.exception("Failed to execute DB script")
        raise
    finally:
        try:
            conn.close()
        except Exception:
            pass
