import sqlite3
from datetime import datetime
import os

DB_PATH = "compliance_audit.db"

def init_db():
    """Initializes the SQLite database and creates the audit_logs table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the audit_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            filename TEXT,
            doc_type TEXT,
            raw_prompt TEXT,
            raw_response TEXT,
            status TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def log_audit(filename: str, doc_type: str, prompt: str, response: str, status: str = "Success"):
    """
    Logs the LLM interaction to the database for auditing and debugging.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    cursor.execute('''
        INSERT INTO audit_logs (timestamp, filename, doc_type, raw_prompt, raw_response, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, filename, doc_type, prompt, response, status))
    
    conn.commit()
    conn.close()

def fetch_all_logs():
    """Utility to retrieve logs for the UI or debugging."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Automatically initialize when this module is imported
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")