import uuid
from typing import List, Optional
from psycopg2.extras import RealDictCursor


class SessionCRUD:
    """
    Data access layer for editor sessions. Uses psycopg2 for direct SQL
    statements in keeping with the rest of the application.
    """

    def create_session(
        self, user_id: int, name: str, data: str, db
    ) -> Optional[dict]:
        """
        Create a new editing session for the given user.

        :param user_id: ID of the user who owns the session
        :param name: A human friendly name for the session
        :param data: A JSON string representing the report/session contents
        :param db: Database connection
        :return: The created session row as a dict

        This implementation sets both ``created_at`` and ``updated_at`` to the
        current timestamp using ``NOW()`` so that they are never ``NULL``.
        """
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            session_id = str(uuid.uuid4())
            # Insert a new session, explicitly populating created_at and updated_at
            cursor.execute(
                """
                INSERT INTO editor_sessions (
                    id, user_id, name, data, created_at, updated_at
                )
                VALUES (
                    %(id)s,
                    %(user_id)s,
                    %(name)s,
                    %(data)s,
                    NOW(),
                    NOW()
                )
                RETURNING *
                """,
                {
                    "id": session_id,
                    "user_id": user_id,
                    "name": name,
                    "data": data,
                },
            )
            row = cursor.fetchone()
            db.commit()
            return row
        except Exception:
            db.rollback()
            raise
        finally:
            cursor.close()

    def get_sessions_by_user(self, user_id: int, db) -> List[dict]:
        """
        Retrieve all sessions belonging to a user, ordered by most recently
        updated first.
        """
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(
                """
                SELECT id, name, created_at, updated_at
                FROM editor_sessions
                WHERE user_id = %(user_id)s
                ORDER BY updated_at DESC
                """,
                {"user_id": user_id},
            )
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_session_by_id(
        self, session_id: str, user_id: int, db
    ) -> Optional[dict]:
        """
        Fetch a single session by its ID if it belongs to the given user.
        """
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(
                """
                SELECT *
                FROM editor_sessions
                WHERE id = %(id)s AND user_id = %(user_id)s
                """,
                {"id": session_id, "user_id": user_id},
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def update_session(
        self, session_id: str, user_id: int, name: str, data: str, db
    ) -> Optional[dict]:
        """
        Update an existing session's name and data. Only sessions owned by
        the user can be updated.
        """
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(
                """
                UPDATE editor_sessions
                SET name = %(name)s,
                    data = %(data)s,
                    updated_at = now()
                WHERE id = %(id)s AND user_id = %(user_id)s
                RETURNING *
                """,
                {
                    "id": session_id,
                    "user_id": user_id,
                    "name": name,
                    "data": data,
                },
            )
            row = cursor.fetchone()
            if row:
                db.commit()
            return row
        except Exception:
            db.rollback()
            raise
        finally:
            cursor.close()


session_crud = SessionCRUD()