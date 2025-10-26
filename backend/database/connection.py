import logging
import psycopg2
from psycopg2 import pool, extensions
from core.config import settings

class DatabaseConnection:
    _initialized = False
    connection_pool = None

    def __init__(self):
        if not self._initialized:
            self.initialize_pool()
            self._initialized = True

    def initialize_pool(self):
        try:
            # Use configured pool size from settings
            # Default: min=2, max=20 (sufficient for concurrent PDF processing)
            min_connections = settings.DB_POOL_MIN_CONN
            max_connections = settings.DB_POOL_MAX_CONN

            if settings.DATABASE_URL:
                # If DATABASE_URL is provided in the settings, use it
                # Add keepalive parameters to prevent stale connections
                self.connection_pool = pool.SimpleConnectionPool(
                    min_connections, max_connections,
                    settings.DATABASE_URL,
                    keepalives=1,
                    keepalives_idle=30,
                    keepalives_interval=10,
                    keepalives_count=5,
                    connect_timeout=10
                )
            else:
                # Fallback to individual parameters if DATABASE_URL is not provided
                db_config = {
                    "host": settings.NEON_HOST,
                    "database": settings.NEON_DATABASE,
                    "user": settings.NEON_USER,
                    "password": settings.NEON_PASSWORD,
                    "port": settings.NEON_PORT,
                    "sslmode": "require",
                    "keepalives": 1,
                    "keepalives_idle": 30,
                    "keepalives_interval": 10,
                    "keepalives_count": 5,
                    "connect_timeout": 10,
                }
                self.connection_pool = pool.SimpleConnectionPool(min_connections, max_connections, **db_config)

            logging.info(f"✅ Database connection pool created successfully (min={min_connections}, max={max_connections}) with keepalive enabled")
        except Exception as error:
            logging.error(f"❌ Error creating database connection pool: {error}")
            raise

    def get_connection(self):
        """Retrieve a connection from the pool with health validation."""
        max_retries = 3
        last_error = None

        # Log pool statistics before attempting to get connection
        try:
            pool_info = self.get_pool_stats()
            logging.debug(f"Pool stats before get_connection: {pool_info}")
        except Exception as e:
            logging.warning(f"Could not get pool stats: {e}")

        for attempt in range(max_retries):
            try:
                connection = self.connection_pool.getconn()

                # Check if connection is closed
                if connection.closed != 0:
                    logging.warning(f"⚠️ Connection is closed (attempt {attempt + 1}/{max_retries})")
                    self.connection_pool.putconn(connection, close=True)
                    continue

                # Validate connection health with a test query
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT 1")
                        cursor.fetchone()

                    # Reset connection state before use
                    connection.rollback()
                    return connection

                except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                    logging.warning(f"⚠️ Connection health check failed (attempt {attempt + 1}/{max_retries}): {e}")
                    # Close the bad connection and remove it from pool
                    self.connection_pool.putconn(connection, close=True)
                    last_error = e
                    continue

            except pool.PoolError as e:
                # Pool exhausted - log detailed stats
                pool_stats = self.get_pool_stats()
                logging.error(f"❌ Connection pool exhausted (attempt {attempt + 1}/{max_retries}): {pool_stats}")
                last_error = e
                if attempt < max_retries - 1:
                    import time
                    time.sleep(0.1)  # Brief wait before retry
                    continue
            except Exception as e:
                logging.error(f"❌ Error getting connection from pool (attempt {attempt + 1}/{max_retries}): {e}")
                last_error = e
                if attempt < max_retries - 1:
                    continue

        # All retries exhausted
        pool_stats = self.get_pool_stats()
        error_msg = f"Failed to get healthy connection after {max_retries} attempts. Pool stats: {pool_stats}"
        if last_error:
            error_msg += f". Last error: {last_error}"
        logging.error(f"❌ {error_msg}")
        raise psycopg2.OperationalError(error_msg)

    def return_connection(self, connection):
        """Return the connection to the pool after resetting its state."""
        if connection:
            try:
                # Ensure connection is in clean state before returning to pool
                if connection.closed == 0:
                    # Rollback any uncommitted transactions
                    if connection.get_transaction_status() != psycopg2.extensions.TRANSACTION_STATUS_IDLE:
                        connection.rollback()
                    self.connection_pool.putconn(connection)
                else:
                    # Connection is closed, remove it from pool
                    logging.warning("⚠️ Returning closed connection, removing from pool")
                    self.connection_pool.putconn(connection, close=True)
            except Exception as e:
                logging.error(f"❌ Error returning connection to pool: {e}")
                try:
                    self.connection_pool.putconn(connection, close=True)
                except Exception:
                    pass

    def close_all_connections(self):
        """Close all connections in the pool."""
        if self.connection_pool:
            self.connection_pool.closeall()
            logging.info("✅ All connections closed")

    def is_connection_alive(self):
        """Check if a connection to the database is alive."""
        connection = None
        try:
            connection = self.get_connection()
            if not connection:
                return False
            # Connection validation already done in get_connection()
            return True
        except psycopg2.OperationalError as e:
            logging.error(f"❌ OperationalError during connection check: {e}")
            return False
        except Exception as e:
            logging.error(f"❌ Unexpected error during connection check: {e}")
            return False
        finally:
            if connection:
                self.return_connection(connection)

    def validate_pool_health(self):
        """Validate and clean up stale connections in the pool."""
        if not self.connection_pool:
            return

        logging.info("🔍 Starting connection pool health check...")
        try:
            # Test a connection from the pool
            if self.is_connection_alive():
                logging.info("✅ Connection pool health check passed")
            else:
                logging.warning("⚠️ Connection pool health check failed, reinitializing...")
                self.close_all_connections()
                self.initialize_pool()
        except Exception as e:
            logging.error(f"❌ Error during pool health validation: {e}")
            # Try to reinitialize pool
            try:
                self.close_all_connections()
                self.initialize_pool()
            except Exception as reinit_error:
                logging.error(f"❌ Failed to reinitialize pool: {reinit_error}")

    def get_pool_stats(self) -> dict:
        """Get current connection pool statistics for monitoring."""
        if not self.connection_pool:
            return {"status": "not_initialized"}

        try:
            # SimpleConnectionPool stores connections in _pool (list)
            # and tracks used connections in _used (dict)
            pool_obj = self.connection_pool
            total_connections = len(pool_obj._pool) + len(pool_obj._used)
            available = len(pool_obj._pool)
            in_use = len(pool_obj._used)

            return {
                "total": total_connections,
                "available": available,
                "in_use": in_use,
                "minconn": pool_obj.minconn,
                "maxconn": pool_obj.maxconn,
            }
        except Exception as e:
            return {"error": str(e)}

# Singleton instance
db_manager = DatabaseConnection()
