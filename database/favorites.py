# ============================================================================
# ModernMedia/database/favorites.py v5.0 - Favorites Operations
# ============================================================================

import time

class FavoritesOperations:
    """Favorites database operations"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add(self, file_path, profile='default'):
        """Add to favorites"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    INSERT OR REPLACE INTO favorites (file_path, profile_name, added_date)
                    VALUES (?, ?, ?)
                ''', (file_path, profile, time.time()))
                self.db.conn.commit()
                return True
        except:
            return False
    
    def remove(self, file_path):
        """Remove from favorites"""
        try:
            with self.db.lock:
                self.db.cursor.execute("DELETE FROM favorites WHERE file_path = ?", (file_path,))
                self.db.conn.commit()
                return True
        except:
            return False
    
    def is_favorite(self, file_path, profile='default'):
        """Check if file is favorite"""
        try:
            with self.db.lock:
                self.db.cursor.execute(
                    "SELECT 1 FROM favorites WHERE file_path = ? AND profile_name = ?",
                    (file_path, profile)
                )
                return self.db.cursor.fetchone() is not None
        except:
            return False
    
    def get_all(self, profile='default', limit=50):
        """Get all favorites"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT file_path, added_date FROM favorites
                    WHERE profile_name = ?
                    ORDER BY added_date DESC LIMIT ?
                ''', (profile, limit))
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def toggle(self, file_path, profile='default'):
        """Toggle favorite status"""
        if self.is_favorite(file_path, profile):
            return self.remove(file_path)
        else:
            return self.add(file_path, profile)
    
    # Bookmark operations (directory favorites)
    def add_bookmark(self, dir_path, name, profile='default'):
        """Add directory bookmark"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    INSERT OR REPLACE INTO bookmarks (dir_path, name, profile_name)
                    VALUES (?, ?, ?)
                ''', (dir_path, name, profile))
                self.db.conn.commit()
                return True
        except:
            return False
    
    def remove_bookmark(self, dir_path):
        """Remove bookmark"""
        try:
            with self.db.lock:
                self.db.cursor.execute("DELETE FROM bookmarks WHERE dir_path = ?", (dir_path,))
                self.db.conn.commit()
                return True
        except:
            return False
    
    def get_bookmarks(self, profile='default'):
        """Get all bookmarks"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT dir_path, name, added_date FROM bookmarks
                    WHERE profile_name = ?
                    ORDER BY name
                ''', (profile,))
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
