# File: database.py - Add these functions to your existing database.py
import sqlite3
from typing import List, Optional, Generator
from model import ReportDocument, ReportBlock
from core.config import DATABASE_URL


def get_db():
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()
def init_reports_db():
    """Initialize reports database tables"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            file_path TEXT,
            file_size INTEGER,
            file_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Report blocks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS report_blocks (
            id TEXT PRIMARY KEY,
            report_id TEXT NOT NULL,
            content TEXT NOT NULL,
            type TEXT DEFAULT 'paragraph',
            block_order INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (report_id) REFERENCES reports (id)
        )
    """)
    
    # Block tags table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS block_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            block_id TEXT NOT NULL,
            tag TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (block_id) REFERENCES report_blocks (id)
        )
    """)
    
    conn.commit()
    conn.close()

def create_report(report: ReportDocument, user_id: int, db) -> bool:
    """Save report to database"""
    try:
        cursor = db.cursor()
        
        # Insert report
        cursor.execute("""
            INSERT INTO reports (id, user_id, title, file_path, file_size, file_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (report.id, user_id, report.title, report.file_path, report.file_size, report.file_type))
        
        # Insert blocks
        for i, block in enumerate(report.blocks):
            cursor.execute("""
                INSERT INTO report_blocks (id, report_id, content, type, block_order)
                VALUES (?, ?, ?, ?, ?)
            """, (block.id, report.id, block.content, block.type, i))
            
            # Insert tags for this block
            for tag in block.tags:
                cursor.execute("""
                    INSERT INTO block_tags (block_id, tag)
                    VALUES (?, ?)
                """, (block.id, tag))
        
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()
        raise e

def get_reports_by_user(user_id: int, db) -> List[ReportDocument]:
    """Get all reports for a user"""
    cursor = db.cursor()
    
    # Get reports
    cursor.execute("""
        SELECT id, title, file_path, file_size, file_type, created_at, updated_at
        FROM reports WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    
    reports = []
    for report_row in cursor.fetchall():
        report_id = report_row[0]
        
        # Get blocks for this report
        cursor.execute("""
            SELECT rb.id, rb.content, rb.type, rb.block_order
            FROM report_blocks rb
            WHERE rb.report_id = ?
            ORDER BY rb.block_order
        """, (report_id,))
        
        blocks = []
        for block_row in cursor.fetchall():
            block_id = block_row[0]
            
            # Get tags for this block
            cursor.execute("""
                SELECT tag FROM block_tags WHERE block_id = ?
            """, (block_id,))
            tags = [tag[0] for tag in cursor.fetchall()]
            
            blocks.append(ReportBlock(
                id=block_id,
                content=block_row[1],
                type=block_row[2],
                tags=tags
            ))
        
        reports.append(ReportDocument(
            id=report_id,
            title=report_row[1],
            file_path=report_row[2],
            file_size=report_row[3],
            file_type=report_row[4],
            created_at=report_row[5],
            updated_at=report_row[6],
            blocks=blocks
        ))
    
    return reports

def delete_report(report_id: str, user_id: int, db) -> Optional[str]:
    """Delete a report and return file path if exists"""
    cursor = db.cursor()
    
    # Check if report exists and belongs to user
    cursor.execute("""
        SELECT file_path FROM reports 
        WHERE id = ? AND user_id = ?
    """, (report_id, user_id))
    
    result = cursor.fetchone()
    if not result:
        return None
    
    file_path = result[0]
    
    # Delete from database
    cursor.execute("DELETE FROM block_tags WHERE block_id IN (SELECT id FROM report_blocks WHERE report_id = ?)", (report_id,))
    cursor.execute("DELETE FROM report_blocks WHERE report_id = ?", (report_id,))
    cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    
    db.commit()
    return file_path

# Call this in your main init_db function
def init_db():
    # Your existing init_db code here
    # ...
    
    # Add this line to initialize reports tables
    init_reports_db()

