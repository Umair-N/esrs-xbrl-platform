#!/usr/bin/env python
"""
Quick verification script to check pdf_cache table exists and works.
"""
import sys
sys.path.insert(0, '.')

from database.connection import db_manager

def verify_table():
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cursor:
            # Check if table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'pdf_cache'
                );
            """)
            exists = cursor.fetchone()[0]

            if exists:
                print("✅ pdf_cache table exists!")

                # Check table structure
                cursor.execute("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = 'pdf_cache'
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print("\n📋 Table structure:")
                for col_name, col_type in columns:
                    print(f"   - {col_name}: {col_type}")

                # Check for existing data
                cursor.execute("SELECT COUNT(*) FROM pdf_cache;")
                count = cursor.fetchone()[0]
                print(f"\n📊 Current records: {count}")

                return True
            else:
                print("❌ pdf_cache table does NOT exist!")
                return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db_manager.return_connection(conn)

if __name__ == "__main__":
    success = verify_table()
    sys.exit(0 if success else 1)
