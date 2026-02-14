# ============================================================================
# ModernMedia/database/metadata.py v5.0 - Metadata Operations
# ============================================================================

class MetadataOperations:
    """File metadata operations"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def set(self, file_path, metadata):
        """
        Set file metadata
        
        Args:
            file_path: Path to file
            metadata: dict with keys: title, year, genre, rating, plot,
                     poster_path, duration, resolution, codec, source
        """
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    INSERT OR REPLACE INTO file_metadata 
                    (file_path, title, year, genre, rating, plot, poster_path, 
                     duration, resolution, codec, metadata_source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    file_path,
                    metadata.get('title'),
                    metadata.get('year'),
                    metadata.get('genre'),
                    metadata.get('rating'),
                    metadata.get('plot'),
                    metadata.get('poster_path'),
                    metadata.get('duration'),
                    metadata.get('resolution'),
                    metadata.get('codec'),
                    metadata.get('source', 'manual')
                ))
                self.db.conn.commit()
                return True
        except:
            return False
    
    def get(self, file_path):
        """Get file metadata"""
        try:
            with self.db.lock:
                self.db.cursor.execute(
                    'SELECT * FROM file_metadata WHERE file_path = ?',
                    (file_path,)
                )
                result = self.db.cursor.fetchone()
                return dict(result) if result else None
        except:
            return None
    
    def delete(self, file_path):
        """Delete file metadata"""
        try:
            with self.db.lock:
                self.db.cursor.execute(
                    "DELETE FROM file_metadata WHERE file_path = ?",
                    (file_path,)
                )
                self.db.conn.commit()
                return True
        except:
            return False
    
    def search(self, query, limit=50):
        """Search metadata by title or genre"""
        try:
            with self.db.lock:
                search_term = f"%{query}%"
                self.db.cursor.execute('''
                    SELECT * FROM file_metadata
                    WHERE title LIKE ? OR genre LIKE ? OR plot LIKE ?
                    ORDER BY title
                    LIMIT ?
                ''', (search_term, search_term, search_term, limit))
                
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def get_by_genre(self, genre, limit=50):
        """Get files by genre"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT * FROM file_metadata
                    WHERE genre LIKE ?
                    ORDER BY rating DESC, title
                    LIMIT ?
                ''', (f"%{genre}%", limit))
                
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def get_by_year(self, year, limit=50):
        """Get files by year"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT * FROM file_metadata
                    WHERE year = ?
                    ORDER BY rating DESC, title
                    LIMIT ?
                ''', (year, limit))
                
                return [dict(row) for row in self.db.cursor.fetchall()]
        except:
            return []
    
    def get_all_genres(self):
        """Get list of all genres"""
        try:
            with self.db.lock:
                self.db.cursor.execute('''
                    SELECT DISTINCT genre FROM file_metadata
                    WHERE genre IS NOT NULL
                    ORDER BY genre
                ''')
                return [row['genre'] for row in self.db.cursor.fetchall()]
        except:
            return []
