# ============================================================================
# ModernMedia/database/resume.py v5.0 - Resume Operations
# ============================================================================

import time

class ResumeOperations:
    """Resume point database operations"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get(self, file_path, current_size, current_mtime):
        """
        Get resume data with validation
        
        Returns:
            dict or None
        """
        try:
            with self.db.lock:
                self.db.cursor.execute(
                    "SELECT position_seconds, file_size, mtime FROM resume_points WHERE file_path = ?",
                    (file_path,)
                )
                result = self.db.cursor.fetchone()
                
                if not result:
                    return None
                
                db_data = {
                    'position_seconds': result['position_seconds'],
                    'file_size': result['file_size'],
                    'mtime': result['mtime'],
                }
                
                # Validate file hasn't changed
                mtime_tolerance = 2.0
                if db_data['file_size'] != current_size or \
                   abs(db_data['mtime'] - current_mtime) > mtime_tolerance:
                    # File changed - delete old resume
                    self.delete(file_path)
                    return None
                
                return db_data
        except Exception as e:
            print(f"[DB] Get resume error: {e}")
            return None
    
    def set(self, file_path, position_seconds, file_size, mtime):
        """Save resume position"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    INSERT OR REPLACE INTO resume_points
                    (file_path, position_seconds, file_size, mtime, last_updated)
                    VALUES (?, ?, ?, ?, ?)
                ''', (file_path, position_seconds, file_size, mtime, time.time()))
                self.db.conn.commit()
                return True
        except Exception as e:
            print(f"[DB] Set resume error: {e}")
            return False
    
    def delete(self, file_path):
        """Delete resume point"""
        try:
            with self.db.lock:
                self.db.cursor.execute("DELETE FROM resume_points WHERE file_path = ?", (file_path,))
                self.db.conn.commit()
                return self.db.cursor.rowcount > 0
        except:
            return False
    
    def cleanup_old(self, days=30):
        """Clean up old resume points"""
        try:
            with self.db.lock:
                cutoff = time.time() - (days * 86400)
                self.db.cursor.execute("DELETE FROM resume_points WHERE last_updated < ?", (cutoff,))
                deleted = self.db.cursor.rowcount
                self.db.conn.commit()
                print(f"[DB] Cleaned {deleted} old resume points")
                return deleted
        except:
            return 0
    
    def get_all(self):
        """Get all resume points"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT file_path, position_seconds, last_updated
                    FROM resume_points
                    ORDER BY last_updated DESC
                ''')
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
