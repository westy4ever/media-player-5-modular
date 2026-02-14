# ============================================================================
# ModernMedia/database/playlists.py v5.0 - Playlist Operations
# ============================================================================

class PlaylistOperations:
    """Playlist database operations"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create(self, name, profile='default'):
        """Create new playlist"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    INSERT INTO playlists (name, profile_name) VALUES (?, ?)
                ''', (name, profile))
                self.db.conn.commit()
                return self.db.cursor.lastrowid
        except:
            return None
    
    def delete(self, playlist_id):
        """Delete playlist and its items"""
        try:
            with self.db.lock:
                self.db.cursor.execute("DELETE FROM playlist_items WHERE playlist_id = ?", (playlist_id,))
                self.db.cursor.execute("DELETE FROM playlists WHERE playlist_id = ?", (playlist_id,))
                self.db.conn.commit()
                return True
        except:
            return False
    
    def rename(self, playlist_id, new_name):
        """Rename playlist"""
        try:
            with self.db.lock:
                self.db.cursor.execute(
                    "UPDATE playlists SET name = ? WHERE playlist_id = ?",
                    (new_name, playlist_id)
                )
                self.db.conn.commit()
                return True
        except:
            return False
    
    def get_all(self, profile='default'):
        """Get all playlists"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT playlist_id, name, created FROM playlists
                    WHERE profile_name = ?
                    ORDER BY name
                ''', (profile,))
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def add_item(self, playlist_id, file_path):
        """Add file to playlist"""
        try:
            with self.db.lock:
                # Get next position
                self.db.cursor.execute('''
                    SELECT COALESCE(MAX(position), -1) + 1 as next_pos
                    FROM playlist_items WHERE playlist_id = ?
                ''', (playlist_id,))
                next_pos = self.db.cursor.fetchone()['next_pos']
                
                # Insert
                self.db.cursor.execute('''
                    INSERT INTO playlist_items (playlist_id, file_path, position)
                    VALUES (?, ?, ?)
                ''', (playlist_id, file_path, next_pos))
                self.db.conn.commit()
                return True
        except:
            return False
    
    def remove_item(self, playlist_id, file_path):
        """Remove file from playlist"""
        try:
            with self.db.lock:
                self.db.cursor.execute(
                    "DELETE FROM playlist_items WHERE playlist_id = ? AND file_path = ?",
                    (playlist_id, file_path)
                )
                self.db.conn.commit()
                return True
        except:
            return False
    
    def get_items(self, playlist_id):
        """Get playlist items"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT file_path, position FROM playlist_items
                    WHERE playlist_id = ?
                    ORDER BY position
                ''', (playlist_id,))
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def reorder_items(self, playlist_id, file_paths):
        """Reorder playlist items"""
        try:
            with self.db.lock:
                # Delete existing
                self.db.cursor.execute(
                    "DELETE FROM playlist_items WHERE playlist_id = ?",
                    (playlist_id,)
                )
                
                # Insert in new order
                for position, file_path in enumerate(file_paths):
                    self.db.cursor.execute('''
                        INSERT INTO playlist_items (playlist_id, file_path, position)
                        VALUES (?, ?, ?)
                    ''', (playlist_id, file_path, position))
                
                self.db.conn.commit()
                return True
        except:
            return False
