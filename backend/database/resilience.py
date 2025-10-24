"""
Database resilience utilities for handling transient connection failures.
Provides decorators and helper functions for automatic retry logic.
"""
import logging
import time
from functools import wraps
from typing import Callable, Any

import psycopg2
from psycopg2 import extensions

logger = logging.getLogger(__name__)


def with_db_retry(max_retries: int = 3, delay: float = 0.5):
    """
    Decorator to retry database operations on transient failures.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay in seconds between retries (exponential backoff applied)

    Usage:
        @with_db_retry(max_retries=3, delay=0.5)
        def get_user_by_email(email: str, db):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_error = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)

                except (psycopg2.OperationalError, psycopg2.InterfaceError, psycopg2.DatabaseError) as e:
                    last_error = e
                    error_str = str(e).lower()

                    # Check if this is a transient error that should be retried
                    transient_errors = [
                        "server closed the connection",
                        "connection reset",
                        "connection timed out",
                        "could not connect",
                        "connection refused",
                        "no connection to the server",
                        "ssl connection has been closed unexpectedly",
                        "terminating connection due to administrator command"
                    ]

                    is_transient = any(err in error_str for err in transient_errors)

                    if not is_transient or attempt == max_retries - 1:
                        logger.error(f"❌ Database operation failed after {attempt + 1} attempts: {e}")
                        raise

                    # Log retry attempt
                    wait_time = delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(
                        f"⚠️ Transient database error (attempt {attempt + 1}/{max_retries}): {e}. "
                        f"Retrying in {wait_time:.2f}s..."
                    )

                    # Reset connection in kwargs if present
                    if 'db' in kwargs:
                        conn = kwargs['db']
                        try:
                            if conn and conn.closed == 0:
                                conn.rollback()
                        except Exception:
                            pass

                    # Check args for db connection
                    for arg in args:
                        if hasattr(arg, 'closed') and hasattr(arg, 'rollback'):
                            try:
                                if arg.closed == 0:
                                    arg.rollback()
                            except Exception:
                                pass

                    time.sleep(wait_time)

                except Exception as e:
                    # Non-transient error, raise immediately
                    logger.error(f"❌ Non-transient error in database operation: {e}")
                    raise

            # Should never reach here, but just in case
            raise last_error if last_error else Exception("Database operation failed")

        return wrapper
    return decorator


def is_connection_healthy(conn) -> bool:
    """
    Check if a database connection is healthy and ready to use.

    Args:
        conn: psycopg2 connection object

    Returns:
        bool: True if connection is healthy, False otherwise
    """
    if not conn:
        return False

    try:
        # Check if connection is closed
        if conn.closed != 0:
            return False

        # Check transaction status
        status = conn.get_transaction_status()
        if status == extensions.TRANSACTION_STATUS_UNKNOWN:
            return False

        # Execute a simple query to verify connection
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return True

    except (psycopg2.OperationalError, psycopg2.InterfaceError, psycopg2.DatabaseError):
        return False
    except Exception as e:
        logger.warning(f"⚠️ Unexpected error checking connection health: {e}")
        return False


def reset_connection_state(conn) -> None:
    """
    Reset a connection to a clean state (rollback any pending transactions).

    Args:
        conn: psycopg2 connection object
    """
    if not conn:
        return

    try:
        if conn.closed == 0:
            status = conn.get_transaction_status()
            if status != extensions.TRANSACTION_STATUS_IDLE:
                conn.rollback()
                logger.debug("🔄 Connection state reset (rolled back pending transaction)")
    except Exception as e:
        logger.warning(f"⚠️ Error resetting connection state: {e}")
