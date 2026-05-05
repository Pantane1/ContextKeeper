import sqlite3
import json
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib
import time

class ContextKeeperDB:
    def __init__(self, db_path="contextkeeper.db"):
        # Add check_same_thread=False to allow multi-threaded access
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS clips (
                id INTEGER PRIMARY KEY,
                content TEXT,
                content_hash TEXT UNIQUE,
                type TEXT,
                timestamp DATETIME,
                session_id INTEGER,
                tags TEXT
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                name TEXT,
                start_time DATETIME,
                end_time DATETIME,
                dominant_topic TEXT
            )
        """)
        self.conn.commit()
    
    def add_clip(self, content, clip_type="text"):
        content_hash = hashlib.md5(content.encode()).hexdigest()
        now = datetime.now()
        
        # Add retry mechanism for locked database
        for attempt in range(3):
            try:
                # Check for duplicate within last 5 seconds
                cursor = self.conn.execute(
                    "SELECT id FROM clips WHERE content_hash = ? AND timestamp > ?",
                    (content_hash, (now - timedelta(seconds=5)).isoformat())
                )
                if cursor.fetchone():
                    return None
                
                # Find or create session
                session_id = self.get_or_create_session(now, content)
                
                # Insert the clip
                cursor = self.conn.execute(
                    "INSERT INTO clips (content, content_hash, type, timestamp, session_id) VALUES (?,?,?,?,?)",
                    (content, content_hash, clip_type, now.isoformat(), session_id)
                )
                self.conn.commit()
                return cursor.lastrowid
                
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < 2:
                    time.sleep(0.1)
                    continue
                raise
    
    def get_or_create_session(self, timestamp, content):
        # Look for recent session (last 2 minutes of inactivity)
        cutoff = timestamp - timedelta(minutes=2)
        cursor = self.conn.execute(
            "SELECT id FROM sessions WHERE end_time IS NULL OR end_time > ? ORDER BY start_time DESC LIMIT 1",
            (cutoff.isoformat(),)
        )
        row = cursor.fetchone()
        if row:
            session_id = row[0]
            # Update end_time
            self.conn.execute(
                "UPDATE sessions SET end_time = ? WHERE id = ?",
                (timestamp.isoformat(), session_id)
            )
            self.conn.commit()
            return session_id
        
        # Create new session
        cursor = self.conn.execute(
            "INSERT INTO sessions (name, start_time, end_time) VALUES (?,?,?)",
            (f"Session {timestamp.strftime('%H:%M')}", timestamp.isoformat(), timestamp.isoformat())
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_recent_sessions(self, limit=10):
        cursor = self.conn.execute("""
            SELECT s.id, s.name, s.start_time, s.end_time,
                   COUNT(c.id) as clip_count,
                   GROUP_CONCAT(c.content, '|||') as contents
            FROM sessions s
            LEFT JOIN clips c ON c.session_id = s.id
            GROUP BY s.id
            ORDER BY s.start_time DESC
            LIMIT ?
        """, (limit,))
        
        sessions = []
        for row in cursor:
            sessions.append({
                'id': row[0],
                'name': row[1],
                'start': row[2],
                'end': row[3],
                'clip_count': row[4],
                'contents': row[5].split('|||') if row[5] else []
            })
        return sessions
    
    def get_session_clips(self, session_id):
        cursor = self.conn.execute(
            "SELECT content, type, timestamp FROM clips WHERE session_id = ? ORDER BY timestamp",
            (session_id,)
        )
        return [{'content': row[0], 'type': row[1], 'timestamp': row[2]} for row in cursor]
    
    def close(self):
        self.conn.close()