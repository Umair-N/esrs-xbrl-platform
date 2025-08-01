from typing import List, Optional

from models.file import FileUpload
from psycopg2.extras import RealDictCursor


class FileCRUD:
    def create_file_record(self, file_data: FileUpload, db) -> Optional[FileUpload]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
                INSERT INTO files (filename, original_filename, file_path, file_size, file_type, user_id)
                VALUES (%(filename)s, %(original_filename)s, %(file_path)s, %(file_size)s, %(file_type)s, %(user_id)s)
                RETURNING *
            """
            cursor.execute(
                query,
                {
                    "filename": file_data.filename,
                    "original_filename": file_data.original_filename,
                    "file_path": file_data.file_path,
                    "file_size": file_data.file_size,
                    "file_type": file_data.file_type,
                    "user_id": file_data.user_id,
                },
            )
            result = cursor.fetchone()
            db.commit()
            return FileUpload(**result) if result else None
        except Exception as error:
            db.rollback()
            raise error
        finally:
            cursor.close()

    def get_user_files(self, user_id: int, db) -> List[FileUpload]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM files WHERE user_id = %(user_id)s ORDER BY created_at DESC"
            cursor.execute(query, {"user_id": user_id})
            results = cursor.fetchall()
            return [FileUpload(**row) for row in results]
        finally:
            cursor.close()

    def get_file_by_id(self, file_id: int, user_id: int, db) -> Optional[FileUpload]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM files WHERE id = %(id)s AND user_id = %(user_id)s"
            cursor.execute(query, {"id": file_id, "user_id": user_id})
            result = cursor.fetchone()
            return FileUpload(**result) if result else None
        finally:
            cursor.close()

    def delete_file(self, file_id: int, user_id: int, db) -> bool:
        cursor = db.cursor()
        try:
            query = "DELETE FROM files WHERE id = %(id)s AND user_id = %(user_id)s"
            cursor.execute(query, {"id": file_id, "user_id": user_id})
            db.commit()
            return cursor.rowcount > 0
        except Exception as error:
            db.rollback()
            raise error
        finally:
            cursor.close()


file_crud = FileCRUD()
