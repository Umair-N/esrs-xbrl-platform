from typing import List, Optional

from models.report import Report, ReportBlock
from psycopg2.extras import RealDictCursor


class ReportCRUD:
    def create_report_with_blocks(
        self,
        report_id: str,
        title: str,
        user_id: int,
        file_path: Optional[str],
        file_type: Optional[str],
        file_size: Optional[int],
        paragraphs: List[str],
        db,
    ) -> Optional[Report]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            # Insert report
            cursor.execute(
                """
                INSERT INTO reports (id, title, user_id, file_path, file_type, file_size)
                VALUES (%(id)s, %(title)s, %(user_id)s, %(file_path)s, %(file_type)s, %(file_size)s)
                RETURNING *
                """,
                {
                    "id": report_id,
                    "title": title,
                    "user_id": user_id,
                    "file_path": file_path,
                    "file_type": file_type,
                    "file_size": file_size,
                },
            )
            report_row = cursor.fetchone()

            # Insert report blocks
            blocks = []
            for idx, content in enumerate(paragraphs):
                block_id = str(uuid.uuid4())
                cursor.execute(
                    """
                    INSERT INTO report_blocks (id, report_id, content, type, order_index, tags)
                    VALUES (%(id)s, %(report_id)s, %(content)s, %(type)s, %(order_index)s, %(tags)s)
                    RETURNING *
                    """,
                    {
                        "id": block_id,
                        "report_id": report_id,
                        "content": content,
                        "type": "paragraph",
                        "order_index": idx,
                        "tags": [],
                    },
                )
                block_row = cursor.fetchone()
                blocks.append(ReportBlock(**block_row))

            db.commit()
            report = Report(**report_row)
            report.blocks = blocks
            return report

        except Exception as e:
            db.rollback()
            raise
        finally:
            cursor.close()

    def get_user_reports(self, user_id, db) -> List[Report]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(
                "SELECT * FROM reports WHERE user_id = %(user_id)s ORDER BY created_at DESC",
                {"user_id": user_id},
            )
            rows = cursor.fetchall()
            return [Report(**row) for row in rows]
        finally:
            cursor.close()

    def get_report_by_id(self, report_id, user_id, db) -> Optional[Report]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(
                "SELECT * FROM reports WHERE id = %(id)s AND user_id = %(user_id)s",
                {"id": report_id, "user_id": user_id},
            )
            report_row = cursor.fetchone()
            if not report_row:
                return None
            # get blocks
            cursor.execute(
                "SELECT * FROM report_blocks WHERE report_id = %(report_id)s ORDER BY order_index",
                {"report_id": report_id},
            )
            block_rows = cursor.fetchall()
            report = Report(**report_row)
            report.blocks = [ReportBlock(**b) for b in block_rows]
            return report
        finally:
            cursor.close()

    def delete_report(self, report_id, user_id, db) -> Optional[str]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            # Find file_path before deletion
            cursor.execute(
                "SELECT file_path FROM reports WHERE id = %(id)s AND user_id = %(user_id)s",
                {"id": report_id, "user_id": user_id},
            )
            row = cursor.fetchone()
            file_path = row["file_path"] if row else None

            cursor.execute(
                "DELETE FROM reports WHERE id = %(id)s AND user_id = %(user_id)s",
                {"id": report_id, "user_id": user_id},
            )
            db.commit()
            return file_path
        except Exception as e:
            db.rollback()
            raise
        finally:
            cursor.close()


import uuid

report_crud = ReportCRUD()
