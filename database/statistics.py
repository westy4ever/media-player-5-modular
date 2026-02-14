# ============================================================================
# ModernMedia/database/statistics.py v5.0 - Statistics Operations
# ============================================================================

import time

class StatisticsOperations:
    """Statistics tracking operations"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def record_view(self, file_path, duration_minutes, profile='default'):
        """Record file view in statistics"""
        try:
            with self.db.lock:
                today = time.strftime('%Y-%m-%d')
                
                self.db.cursor.execute('''
                    INSERT INTO statistics (stat_date, profile_name, files_watched, total_minutes)
                    VALUES (?, ?, 1, ?)
                    ON CONFLICT(stat_date, profile_name) DO UPDATE SET
                        files_watched = files_watched + 1,
                        total_minutes = total_minutes + ?
                ''', (today, profile, duration_minutes, duration_minutes))
                
                self.db.conn.commit()
                return True
        except:
            return False
    
    def get_stats(self, profile='default', days=30):
        """Get viewing statistics"""
        try:
            with self.db.lock:
                cutoff = time.strftime('%Y-%m-%d', time.localtime(time.time() - (days * 86400)))
                
                self.db.cursor.execute('''
                    SELECT SUM(files_watched) as total_files, 
                           SUM(total_minutes) as total_minutes
                    FROM statistics
                    WHERE profile_name = ? AND stat_date >= ?
                ''', (profile, cutoff))
                
                result = self.db.cursor.fetchone()
                return {
                    'total_files': result['total_files'] or 0,
                    'total_minutes': result['total_minutes'] or 0,
                    'total_hours': (result['total_minutes'] or 0) / 60.0
                }
        except:
            return {'total_files': 0, 'total_minutes': 0, 'total_hours': 0}
    
    def get_daily_stats(self, profile='default', days=30):
        """Get day-by-day statistics"""
        try:
            with self.db.lock:
                cutoff = time.strftime('%Y-%m-%d', time.localtime(time.time() - (days * 86400)))
                
                self.db.cursor.execute('''
                    SELECT stat_date, files_watched, total_minutes
                    FROM statistics
                    WHERE profile_name = ? AND stat_date >= ?
                    ORDER BY stat_date DESC
                ''', (profile, cutoff))
                
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def get_most_watched(self, profile='default', limit=10):
        """Get most watched files"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT file_path, COUNT(*) as watch_count,
                           SUM(duration_watched) as total_time
                    FROM watch_history
                    WHERE profile_name = ?
                    GROUP BY file_path
                    ORDER BY watch_count DESC, total_time DESC
                    LIMIT ?
                ''', (profile, limit))
                
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def clear_stats(self, profile='default'):
        """Clear statistics"""
        try:
            with self.db.lock:
                self.db.cursor.execute(
                    "DELETE FROM statistics WHERE profile_name = ?",
                    (profile,)
                )
                self.db.conn.commit()
                return True
        except:
            return False
