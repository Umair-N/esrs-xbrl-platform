from .connection import db_manager


def get_db():
    connection = db_manager.get_connection()
    try:
        yield connection
    finally:
        db_manager.return_connection(connection)
