# ============================================================================
# ModernMedia/database/history.py v5.0 - History Operations
# ============================================================================

import time

class HistoryOperations:
    """Watch history and recent files operations"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    # Recent files
    def add_recent(self, file_path, profile='default'):
        """Add to recent files"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    INSERT OR REPLACE INTO recent_files (file_path, played_date, profile_name)
                    VALUES (?, ?, ?)
                ''', (file_path, time.time(), profile))
                
                # Keep only last 50
                self.db.cursor.execute('''
                    DELETE FROM recent_files WHERE rowid IN (
                        SELECT rowid FROM recent_files 
                        WHERE profile_name = ?
                        ORDER BY played_date DESC 
                        LIMIT -1 OFFSET 50
                    )
                ''', (profile,))
                
                self.db.conn.commit()
                return True
        except:
            return False
    
    def get_recent(self, profile='default', limit=20):
        """Get recent files"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT file_path, played_date FROM recent_files
                    WHERE profile_name = ?
                    ORDER BY played_date DESC LIMIT ?
                ''', (profile, limit))
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def clear_recent(self, profile='default'):
        """Clear recent files"""
        try:
            with self.db.lock:
                self.db.cursor.execute(
                    "DELETE FROM recent_files WHERE profile_name = ?",
                    (profile,)
                )
                self.db.conn.commit()
                return True
        except:
            return False
    
    # Watch history
    def add_watch(self, file_path, duration, profile='default'):
        """Add watch history entry"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    INSERT INTO watch_history (file_path, duration_watched, profile_name, watched_date)
                    VALUES (?, ?, ?, ?)
                ''', (file_path, duration, profile, time.time()))
                
                self.db.conn.commit()
                return True
        except:
            return False
    
    def get_watch_history(self, profile='default', limit=50):
        """Get watch history"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT file_path, watched_date, duration_watched FROM watch_history
                    WHERE profile_name = ?
                    ORDER BY watched_date DESC LIMIT ?
                ''', (profile, limit))
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def get_file_history(self, file_path, profile='default'):
        """Get history for specific file"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT watched_date, duration_watched FROM watch_history
                    WHERE file_path = ? AND profile_name = ?
                    ORDER BY watched_date DESC
                ''', (file_path, profile))
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def clear_watch_history(self, profile='default'):
        """Clear watch history"""
        try:
            with self.db.lock:
                self.db.cursor.execute(
                    "DELETE FROM watch_history WHERE profile_name = ?",
                    (profile,)
                )
                self.db.conn.commit()
                return True
        except:
            return False
