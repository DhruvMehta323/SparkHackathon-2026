from app.core.database import get_connection
from app.core.logger import get_logger

logger = get_logger(__name__)


class BaseRepository:
    @staticmethod
    def fetch_one(query, params=()):
        logger.debug("SQL fetch_one: %s | params=%s", query.strip(), params)
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query, params)
            r = cur.fetchone()
            return dict(r) if r else None
        except Exception:
            logger.exception("fetch_one failed")
            raise
        finally:
            try:
                conn.close()
            except Exception:
                pass

    @staticmethod
    def fetch_all(query, params=()):
        logger.debug("SQL fetch_all: %s | params=%s", query.strip(), params)
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        except Exception:
            logger.exception("fetch_all failed")
            raise
        finally:
            try:
                conn.close()
            except Exception:
                pass

    @staticmethod
    def execute(query, params=()):
        logger.debug("SQL execute: %s | params=%s", query.strip(), params)
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
            return cur.lastrowid
        except Exception:
            logger.exception("execute failed")
            raise
        finally:
            try:
                conn.close()
            except Exception:
                pass
# app/repositories/base.py

from app.core.database import get_connection
from app.core.logger import get_logger

logger = get_logger(__name__)


class BaseRepository:
    """Low-level DB helpers used by all repository classes.

    Methods log queries and parameters to make debugging SQL issues easy.
    They re-raise exceptions after logging so calling code can decide how to
    handle failures.
    """

    @staticmethod
    def fetch_one(query, params=()):
        logger.debug("SQL fetch_one: %s | params=%s", query.strip(), params)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            return dict(result) if result else None
        except Exception:
            logger.exception("fetch_one failed")
            raise
        finally:
            try:
                conn.close()
            except Exception:
                pass

    @staticmethod
    def fetch_all(query, params=()):
        logger.debug("SQL fetch_all: %s | params=%s", query.strip(), params)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception:
            logger.exception("fetch_all failed")
            raise
        finally:
            try:
                conn.close()
            except Exception:
                pass

    @staticmethod
    def execute(query, params=()):
        logger.debug("SQL execute: %s | params=%s", query.strip(), params)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except Exception:
            logger.exception("execute failed")
            raise
        finally:
            try:
                conn.close()
            except Exception:
                pass
