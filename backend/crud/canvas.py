import uuid
from typing import Optional

from psycopg2.extras import RealDictCursor


class CanvasCRUD:
    """
    Data access layer for persisted canvas states. This CRUD operates on
    the ``canvas_states`` table via direct SQL statements to mirror
    existing patterns in the repository. All methods assume the caller
    manages transactions and error handling.
    """

    def create_canvas(
        self,
        user_id: int,
        name: Optional[str],
        data: str,
        report_id: Optional[str],
        db,
    ) -> Optional[dict]:
        """
        Create a new canvas state for the given user.

        :param user_id: ID of the user saving the canvas
        :param name: Human friendly name for the canvas (may be None)
        :param data: Serialized report JSON
        :param report_id: Optional underlying report identifier
        :param db: Database connection
        :return: The created row as a dict

        Both ``created_at`` and ``updated_at`` are set via ``NOW()`` to
        ensure they are never ``NULL``.
        """
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            canvas_id = str(uuid.uuid4())
            cursor.execute(
                """
                INSERT INTO canvas_states (
                    id, user_id, name, data, report_id, created_at, updated_at
                )
                VALUES (
                    %(id)s,
                    %(user_id)s,
                    %(name)s,
                    %(data)s,
                    %(report_id)s,
                    NOW(),
                    NOW()
                )
                RETURNING *
                """,
                {
                    "id": canvas_id,
                    "user_id": user_id,
                    "name": name,
                    "data": data,
                    "report_id": report_id,
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

    def get_canvas_by_id(
        self, canvas_id: str, user_id: int, db
    ) -> Optional[dict]:
        """
        Fetch a saved canvas by its ID, ensuring it belongs to the provided
        user. Returns ``None`` if no matching record is found.
        """
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(
                """
                SELECT *
                FROM canvas_states
                WHERE id = %(id)s AND user_id = %(user_id)s
                """,
                {"id": canvas_id, "user_id": user_id},
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def delete_canvas(
        self, canvas_id: str, user_id: int, db
    ) -> bool:
        """
        Delete a saved canvas owned by the given user. Returns ``True`` if a
        row was removed, otherwise ``False``.
        """
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM canvas_states
                WHERE id = %(id)s AND user_id = %(user_id)s
                """,
                {"id": canvas_id, "user_id": user_id},
            )
            deleted = cursor.rowcount > 0
            if deleted:
                db.commit()
            return deleted
        except Exception:
            db.rollback()
            raise
        finally:
            cursor.close()

    def list_canvases(
        self, user_id: int, db, limit: int = 100, offset: int = 0
    ) -> list[dict]:
        """
        List all canvas states owned by the given user. Results are
        ordered by ``updated_at`` descending so that recently modified
        canvases appear first. Pagination is supported via ``limit``
        and ``offset`` parameters.

        :param user_id: ID of the user to list canvases for
        :param db: Database connection
        :param limit: Maximum number of rows to return
        :param offset: Number of rows to skip before returning results
        :return: A list of canvas rows as dictionaries
        """
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(
                """
                SELECT *
                FROM canvas_states
                WHERE user_id = %(user_id)s
                ORDER BY updated_at DESC
                LIMIT %(limit)s OFFSET %(offset)s
                """,
                {"user_id": user_id, "limit": limit, "offset": offset},
            )
            return cursor.fetchall()
        finally:
            cursor.close()

    def update_canvas(
        self,
        canvas_id: str,
        user_id: int,
        name: Optional[str],
        data: str,
        report_id: Optional[str],
        db,
    ) -> Optional[dict]:
        """
        Update an existing canvas owned by the given user. Only the
        ``name``, ``data`` and ``report_id`` fields are updated; the
        ``updated_at`` timestamp is set to ``NOW()``. Returns the
        updated row or ``None`` if no record matched.

        :param canvas_id: Identifier of the canvas to update
        :param user_id: ID of the owner
        :param name: New name (optional)
        :param data: Serialized report JSON
        :param report_id: Optional report ID to associate
        :param db: Database connection
        :return: The updated row as a dict, or ``None`` if not found
        """
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(
                """
                UPDATE canvas_states
                SET name = %(name)s,
                    data = %(data)s,
                    report_id = %(report_id)s,
                    updated_at = NOW()
                WHERE id = %(id)s AND user_id = %(user_id)s
                RETURNING *
                """,
                {
                    "id": canvas_id,
                    "user_id": user_id,
                    "name": name,
                    "data": data,
                    "report_id": report_id,
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


canvas_crud = CanvasCRUD()