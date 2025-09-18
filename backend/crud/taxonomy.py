from __future__ import annotations

from typing import Optional, List, Dict, Any
from psycopg2.extras import RealDictCursor


class TaxonomyCRUD:
    def create_taxonomy(self, *, name: str, file_name: str, file_path: str, created_by: Optional[int], db) -> Dict[str, Any]:
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                INSERT INTO taxonomies (name, file_name, file_path, created_by, enabled)
                VALUES (%(name)s, %(file_name)s, %(file_path)s, %(created_by)s, TRUE)
                RETURNING id, name, file_name, file_path, enabled, created_at;
            """, {
                "name": name,
                "file_name": file_name,
                "file_path": file_path,
                "created_by": created_by
            })
            row = cur.fetchone()
            db.commit()
            return dict(row) if row else {}
        except Exception:
            db.rollback()
            raise
        finally:
            cur.close()

    def list_taxonomies(self, db) -> List[Dict[str, Any]]:
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                SELECT id, name, file_name, file_path, enabled, created_at
                FROM taxonomies
                ORDER BY created_at DESC;
            """)
            rows = cur.fetchall() or []
            return [dict(r) for r in rows]
        finally:
            cur.close()

    def set_taxonomy_enabled(self, *, taxonomy_id: int, enabled: bool, db) -> None:
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                UPDATE taxonomies
                SET enabled = %(enabled)s
                WHERE id = %(id)s;
            """, {"enabled": enabled, "id": taxonomy_id})
            if cur.rowcount == 0:
                raise ValueError("Taxonomy not found")
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            cur.close()

    def find_taxonomy(self, *, taxonomy_id: int, require_enabled: bool, db) -> Optional[Dict[str, Any]]:
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                SELECT id, name, file_name, file_path, enabled, created_at
                FROM taxonomies
                WHERE id = %(id)s {and_enabled}
                LIMIT 1;
            """.format(and_enabled="AND enabled = TRUE" if require_enabled else ""), {"id": taxonomy_id})
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            cur.close()

    # ---------- User assignments ----------
    def assign_user_taxonomy(self, *, user_id: int, taxonomy_id: int, set_by: Optional[int], db) -> None:
        """
        Assign a taxonomy to a user and make it active.
        - If a taxonomy is already assigned to a user, update it.
        - No longer enforce a single active taxonomy per user.
        """
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            # Check if the taxonomy exists and is enabled
            cur.execute("SELECT id FROM taxonomies WHERE id = %(id)s AND enabled = TRUE;", {"id": taxonomy_id})
            if cur.fetchone() is None:
                raise ValueError("Taxonomy not found or disabled")

            # Disable all active taxonomies for this user (if needed)
            cur.execute("""
                UPDATE user_taxonomies
                SET enabled = FALSE, updated_at = NOW()
                WHERE user_id = %(user_id)s AND enabled = TRUE;
            """, {"user_id": user_id})

            # Now insert or update the selected taxonomy to make it active
            cur.execute("""
                INSERT INTO user_taxonomies (user_id, taxonomy_id, enabled, set_by, updated_at)
                VALUES (%(user_id)s, %(taxonomy_id)s, TRUE, %(set_by)s, NOW())
                ON CONFLICT (user_id, taxonomy_id)
                DO UPDATE SET enabled = EXCLUDED.enabled, set_by = EXCLUDED.set_by, updated_at = NOW();
            """, {"user_id": user_id, "taxonomy_id": taxonomy_id, "set_by": set_by})

            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            cur.close()


    def disable_user_taxonomy(self, *, user_id: int, db) -> int:
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                UPDATE user_taxonomies
                SET enabled = FALSE, updated_at = NOW()
                WHERE user_id = %(user_id)s AND enabled = TRUE;
            """, {"user_id": user_id})
            count = cur.rowcount or 0
            db.commit()
            return count
        except Exception:
            db.rollback()
            raise
        finally:
            cur.close()

    def resolve_active_taxonomy_path(self, *, user_id: int, db) -> str:
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                SELECT t.file_path
                FROM user_taxonomies ut
                JOIN taxonomies t ON t.id = ut.taxonomy_id
                WHERE ut.user_id = %(uid)s AND ut.enabled = TRUE AND t.enabled = TRUE
                ORDER BY t.created_at DESC
                LIMIT 1;
            """, {"uid": user_id})
            row = cur.fetchone()
            if row and row.get("file_path"):
                return row["file_path"]  # This will return the relative file path

            # Fallback for global taxonomy
            cur.execute("""
                SELECT file_path
                FROM taxonomies
                WHERE enabled = TRUE
                ORDER BY created_at DESC
                LIMIT 1;
            """)
            row = cur.fetchone()
            return row["file_path"] if row and row.get("file_path") else ""
        finally:
            cur.close()


    def get_user_active_taxonomy(self, *, user_id: int, db) -> Optional[Dict[str, Any]]:
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                SELECT t.id, t.name, t.file_name, t.file_path, t.enabled, t.created_at
                FROM user_taxonomies ut
                JOIN taxonomies t ON t.id = ut.taxonomy_id
                WHERE ut.user_id = %(uid)s AND ut.enabled = TRUE AND t.enabled = TRUE
                ORDER BY t.created_at DESC
                LIMIT 1;
            """, {"uid": user_id})
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            cur.close()

    def get_user_taxonomies(self, user_id: int, db) -> List[Dict[str, Any]]:
        """Get all enabled taxonomies assigned to a user."""
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                SELECT t.id, t.name, t.file_name, t.file_path, t.enabled, t.created_at
                FROM user_taxonomies ut
                JOIN taxonomies t ON t.id = ut.taxonomy_id
                WHERE ut.user_id = %(uid)s
                AND t.enabled = TRUE
                ORDER BY t.created_at DESC;
            """, {"uid": user_id})
            rows = cur.fetchall()
            return rows if rows else []
        finally:
            cur.close()

    def switch_taxonomy(self, user_id: int, taxonomy_id: int, db) -> None:
        """Switch the active taxonomy for a user."""
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            # Disable all active taxonomies for this user
            cur.execute("""
                UPDATE user_taxonomies
                SET enabled = FALSE
                WHERE user_id = %(user_id)s;
            """, {"user_id": user_id})

            # Enable the selected taxonomy for the user
            cur.execute("""
                UPDATE user_taxonomies
                SET enabled = TRUE
                WHERE user_id = %(user_id)s AND taxonomy_id = %(taxonomy_id)s;
            """, {"user_id": user_id, "taxonomy_id": taxonomy_id})
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cur.close()
    def set_user_active_taxonomy(self, *, user_id: int, taxonomy_id: int, set_by: Optional[int], db) -> None:
        """
        Assign a taxonomy to a user and make it active.
        - No longer enforce a single active taxonomy per user.
        - Allows multiple active taxonomies for the user.
        """
        cur = db.cursor(cursor_factory=RealDictCursor)
        try:
            # Ensure the taxonomy exists and is enabled
            cur.execute("SELECT id FROM taxonomies WHERE id = %(id)s AND enabled = TRUE;", {"id": taxonomy_id})
            if cur.fetchone() is None:
                raise ValueError("Taxonomy not found or disabled")

            # Insert or update the taxonomy for the user, making it active (enabled = TRUE)
            cur.execute("""
                INSERT INTO user_taxonomies (user_id, taxonomy_id, enabled, set_by, updated_at)
                VALUES (%(user_id)s, %(taxonomy_id)s, TRUE, %(set_by)s, NOW())
                ON CONFLICT (user_id, taxonomy_id)
                DO UPDATE SET enabled = EXCLUDED.enabled, set_by = EXCLUDED.set_by, updated_at = NOW();
            """, {"user_id": user_id, "taxonomy_id": taxonomy_id, "set_by": set_by})

            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            cur.close()

    

taxonomy_crud = TaxonomyCRUD()
