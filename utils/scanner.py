# ============================================================================
# ModernMedia/utils/scanner.py v5.0 - Directory Scanner
# ============================================================================

import os
import stat
import threading
from ..constants import MEDIA_EXTENSIONS

class DirectoryScanner(threading.Thread):
    """
    Threaded directory scanner
    Scans for media files and directories without blocking UI
    """
    
    def __init__(self, path, db=None, media_ext=MEDIA_EXTENSIONS, 
                 search_query="", cache=None):
        threading.Thread.__init__(self)
        self.daemon = True
        
        self.path = path
        self.db = db
        self.media_ext = media_ext
        self.search_query = search_query
        self.cache = cache
        
        self.results = None
        self.exception = None
        self.stop_event = threading.Event()
    
    def run(self):
        """Scan directory"""
        # Check cache first
        if self.cache and not self.search_query:
            cached = self.cache.get_dir(self.path)
            if cached:
                self.results = cached
                return
        
        items = []
        
        try:
            for item in sorted(os.listdir(self.path)):
                # Check for stop signal
                if self.stop_event.is_set():
                    break
                
                # Handle bytes encoding
                if isinstance(item, bytes):
                    try:
                        item = item.decode('utf-8')
                    except:
                        continue
                
                # Skip hidden files
                if item.startswith('.'):
                    continue
                
                full_path = os.path.join(self.path, item)
                
                # Get file stats
                try:
                    stats = os.stat(full_path)
                except:
                    continue
                
                # Directory
                if stat.S_ISDIR(stats.st_mode):
                    items.append((
                        item,
                        full_path,
                        'dir',
                        None,
                        None,
                        0
                    ))
                
                # Media file
                elif stat.S_ISREG(stats.st_mode) and item.lower().endswith(self.media_ext):
                    resume_sec = 0
                    is_fav = False
                    
                    # Get resume data
                    if self.db:
                        try:
                            resume_data = self.db.resume.get(
                                full_path, stats.st_size, stats.st_mtime
                            )
                            resume_sec = resume_data.get('position_seconds', 0) if resume_data else 0
                            is_fav = self.db.favorites.is_favorite(full_path)
                        except:
                            pass
                    
                    # Build display name
                    display = item
                    if is_fav:
                        display = "★ " + display
                    
                    items.append((
                        display,
                        full_path,
                        'file',
                        stats.st_size,
                        stats.st_mtime,
                        resume_sec
                    ))
        
        except Exception as e:
            self.exception = e
        
        # Cache results
        if self.cache and not self.search_query:
            self.cache.set_dir(self.path, items)
        
        self.results = items
    
    def stop(self):
        """Stop scanning"""
        self.stop_event.set()
    
    def is_alive(self):
        """Check if still running"""
        return threading.Thread.is_alive(self)
