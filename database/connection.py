# ============================================================================
# ModernMedia/database/connection.py v5.0 - Database Manager
# ============================================================================

import sqlite3
import os
import threading
from ..constants import DB_PATHS

def get_db_path():
    """Find writable database path"""
    for path in DB_PATHS:
        db_dir = os.path.dirname(path)
        try:
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            
            # Test write access
            test_file = os.path.join(db_dir, ".write_test")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("test")
            os.remove(test_file)
            
            print(f"[DB] Using: {path}")
            return path
        except:
            continue
    
    print("[DB] WARNING: Using /tmp (not persistent)")
    return "/tmp/modernmedia_v5.db"

class DatabaseManager:
    """
    Main database manager
    Provides access to all database operations through modules
    """
    
    def __init__(self):
        self.db_path = get_db_path()
        self.conn = None
        self.cursor = None
        self.lock = threading.RLock()
        
        # Initialize connection
        self.connect()
        self.create_tables()
        
        # Import operation modules
        from .resume import ResumeOperations
        from .favorites import FavoritesOperations
        from .playlists import PlaylistOperations
        from .history import HistoryOperations
        from .statistics import StatisticsOperations
        from .metadata import MetadataOperations
        
        # Initialize modules
        self.resume = ResumeOperations(self)
        self.favorites = FavoritesOperations(self)
        self.playlists = PlaylistOperations(self)
        self.history = HistoryOperations(self)
        self.statistics = StatisticsOperations(self)
        self.metadata = MetadataOperations(self)
    
    def connect(self):
        """Establish database connection"""
        try:
            db_dir = os.path.dirname(self.db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.conn.text_factory = str
            
            # Performance settings
            self.conn.execute("PRAGMA journal_mode = WAL")
            self.conn.execute("PRAGMA synchronous = NORMAL")
            self.conn.execute("PRAGMA cache_size = -10000")
            self.conn.execute("PRAGMA temp_store = MEMORY")
            
            self.cursor = self.conn.cursor()
            print(f"[DB] Connected: {self.db_path}")
        except Exception as e:
            raise Exception(f"DB connection failed: {e}")
    
    def create_tables(self):
        """Create all database tables"""
        try:
            with self.lock:
                # Resume points
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS resume_points (
                        file_path TEXT PRIMARY KEY,
                        position_seconds INTEGER,
                        file_size INTEGER,
                        mtime REAL,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Favorites
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS favorites (
                        file_path TEXT PRIMARY KEY,
                        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        profile_name TEXT DEFAULT 'default'
                    )
                ''')
                
                # Bookmarks
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bookmarks (
                        dir_path TEXT PRIMARY KEY,
                        name TEXT,
                        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        profile_name TEXT DEFAULT 'default'
                    )
                ''')
                
                # Playlists
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS playlists (
                        playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        profile_name TEXT DEFAULT 'default'
                    )
                ''')
                
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS playlist_items (
                        playlist_id INTEGER,
                        file_path TEXT,
                        position INTEGER,
                        FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id) ON DELETE CASCADE
                    )
                ''')
                
                # Recent files
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS recent_files (
                        file_path TEXT PRIMARY KEY,
                        played_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        profile_name TEXT DEFAULT 'default'
                    )
                ''')
                
                # Watch history
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS watch_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_path TEXT,
                        watched_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        duration_watched INTEGER,
                        profile_name TEXT DEFAULT 'default'
                    )
                ''')
                
                # Statistics
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS statistics (
                        stat_date DATE,
                        profile_name TEXT,
                        files_watched INTEGER DEFAULT 0,
                        total_minutes INTEGER DEFAULT 0,
                        PRIMARY KEY (stat_date, profile_name)
                    )
                ''')
                
                # File metadata
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS file_metadata (
                        file_path TEXT PRIMARY KEY,
                        title TEXT,
                        year INTEGER,
                        genre TEXT,
                        rating REAL,
                        plot TEXT,
                        poster_path TEXT,
                        duration INTEGER,
                        resolution TEXT,
                        codec TEXT,
                        metadata_source TEXT,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # User profiles
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS profiles (
                        profile_name TEXT PRIMARY KEY,
                        display_name TEXT,
                        pin TEXT,
                        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_active TIMESTAMP
                    )
                ''')
                
                # Default profile
                self.cursor.execute('''
                    INSERT OR IGNORE INTO profiles (profile_name, display_name)
                    VALUES ('default', 'Default User')
                ''')
                
                # Indexes
                self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_recent_date ON recent_files(played_date DESC)')
                self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_date ON watch_history(watched_date DESC)')
                self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_favorites_profile ON favorites(profile_name)')
                self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_resume_updated ON resume_points(last_updated)')
                
                self.conn.commit()
                print("[DB] Tables created ✓")
        except Exception as e:
            raise Exception(f"Table creation failed: {e}")
    
    def execute(self, query, params=()):
        """Execute query with lock"""
        with self.lock:
            self.cursor.execute(query, params)
            return self.cursor
    
    def commit(self):
        """Commit transaction"""
        with self.lock:
            self.conn.commit()
    
    def optimize(self):
        """Optimize database"""
        try:
            with self.lock:
                self.cursor.execute("ANALYZE")
                self.cursor.execute("PRAGMA optimize")
                self.conn.commit()
                print("[DB] Optimized ✓")
                return True
        except:
            return False
    
    def vacuum(self):
        """Vacuum database"""
        try:
            with self.lock:
                self.cursor.execute("VACUUM")
                self.conn.commit()
                print("[DB] Vacuumed ✓")
                return True
        except:
            return False
    
    def get_size(self):
        """Get database file size in bytes"""
        try:
            return os.path.getsize(self.db_path)
        except:
            return 0
    
    def get_size_mb(self):
        """Get database size in MB"""
        return self.get_size() / (1024 ** 2)
    
    def backup(self, backup_path):
        """Backup database"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            print(f"[DB] Backed up to {backup_path}")
            return True
        except:
            return False
    
    def close(self):
        """Close database connection"""
        try:
            if self.conn:
                self.conn.close()
                print("[DB] Closed")
        except:
            pass
    
    def __del__(self):
        self.close()
