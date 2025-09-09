# crud/context.py
from __future__ import annotations
from typing import Optional, List, Dict, Any
from psycopg2.extras import RealDictCursor


class ContextCRUD:
    def create(self, payload: Dict[str, Any], db) -> Optional[Dict[str, Any]]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            INSERT INTO xbrl_contexts (
                user_id,
                context_id, entity_scheme, entity_identifier, entity_name, lei,
                period_type, start_date, end_date, instant_date,
                dimensions_json, taxonomy_id, content_hash,
                is_default_context, status, validation_messages
            )
            VALUES (
                %(user_id)s,
                %(context_id)s, %(entity_scheme)s, %(entity_identifier)s, %(entity_name)s, %(lei)s,
                %(period_type)s, %(start_date)s, %(end_date)s, %(instant_date)s,
                %(dimensions_json)s, %(taxonomy_id)s, %(content_hash)s,
                %(is_default_context)s, %(status)s, %(validation_messages)s
            )
            ON CONFLICT (user_id, content_hash) DO UPDATE SET
                entity_name = EXCLUDED.entity_name,
                lei = EXCLUDED.lei,
                taxonomy_id = COALESCE(EXCLUDED.taxonomy_id, xbrl_contexts.taxonomy_id),
                is_default_context = EXCLUDED.is_default_context,
                status = EXCLUDED.status,
                validation_messages = EXCLUDED.validation_messages
            RETURNING *;
            """
            cursor.execute(query, payload)
            row = cursor.fetchone()
            db.commit()
            return row
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    def bulk_upsert(self, rows: List[Dict[str, Any]], db) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for r in rows:
            out.append(self.create(r, db))
        return out

    def get_by_id(self, ctx_id: int, user_id: int, db) -> Optional[Dict[str, Any]]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(
                "SELECT * FROM xbrl_contexts WHERE id = %(id)s AND user_id = %(user_id)s",
                {"id": ctx_id, "user_id": user_id},
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def list(self, filters: Dict[str, Any], user_id: int, db) -> List[Dict[str, Any]]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            clauses = ["user_id = %(user_id)s"]
            params: Dict[str, Any] = {"user_id": user_id}

            if filters.get("entity_identifier"):
                clauses.append("entity_identifier = %(entity_identifier)s")
                params["entity_identifier"] = filters["entity_identifier"]
            if filters.get("period_type"):
                clauses.append("period_type = %(period_type)s")
                params["period_type"] = filters["period_type"]
            if filters.get("taxonomy_id") is not None:
                clauses.append("taxonomy_id = %(taxonomy_id)s")
                params["taxonomy_id"] = filters["taxonomy_id"]
            if filters.get("context_id"):
                clauses.append("context_id = %(context_id)s")
                params["context_id"] = filters["context_id"]
            if filters.get("date_from"):
                clauses.append("( (period_type = 'instant' AND instant_date >= %(date_from)s) OR (period_type = 'duration' AND end_date >= %(date_from)s) )")
                params["date_from"] = filters["date_from"]
            if filters.get("date_to"):
                clauses.append("( (period_type = 'instant' AND instant_date <= %(date_to)s) OR (period_type = 'duration' AND end_date <= %(date_to)s) )")
                params["date_to"] = filters["date_to"]
            if filters.get("is_default_context") is not None:
                clauses.append("is_default_context = %(is_default_context)s")
                params["is_default_context"] = filters["is_default_context"]

            where_sql = f"WHERE {' AND '.join(clauses)}"
            limit = int(filters.get("limit", 50))
            offset = int(filters.get("offset", 0))
            query = f"""
                SELECT * FROM xbrl_contexts
                {where_sql}
                ORDER BY updated_at DESC
                LIMIT {limit} OFFSET {offset}
            """
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()

    def update_partial(self, ctx_id: int, user_id: int, data: Dict[str, Any], db) -> Optional[Dict[str, Any]]:
        if not data:
            return self.get_by_id(ctx_id, user_id, db)
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            sets = []
            params = {"id": ctx_id, "user_id": user_id}
            for k, v in data.items():
                sets.append(f"{k} = %({k})s")
                params[k] = v
            set_sql = ", ".join(sets)
            query = f"""
                UPDATE xbrl_contexts
                SET {set_sql}
                WHERE id = %(id)s AND user_id = %(user_id)s
                RETURNING *;
            """
            cursor.execute(query, params)
            row = cursor.fetchone()
            db.commit()
            return row
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()

    def delete(self, ctx_id: int, user_id: int, db) -> bool:
        cursor = db.cursor()
        try:
            cursor.execute(
                "DELETE FROM xbrl_contexts WHERE id = %(id)s AND user_id = %(user_id)s",
                {"id": ctx_id, "user_id": user_id},
            )
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()


context_crud = ContextCRUD()
