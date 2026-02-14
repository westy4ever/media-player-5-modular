# ============================================================================
# ModernMedia/utils/cache.py v5.0 - Smart Caching System
# ============================================================================

import time
import threading
from ..constants import CACHE_TTL

class SmartCache:
    """
    Intelligent caching system for directory listings
    Thread-safe with TTL expiration
    """
    
    def __init__(self, ttl=CACHE_TTL):
        self.dir_cache = {}
        self.meta_cache = {}
        self.ttl = ttl
        self.lock = threading.RLock()
    
    def get_dir(self, path):
        """Get cached directory listing"""
        with self.lock:
            if path in self.dir_cache:
                entry = self.dir_cache[path]
                if time.time() - entry['time'] < self.ttl:
                    return entry['data']
                else:
                    # Expired - remove
                    del self.dir_cache[path]
        return None
    
    def set_dir(self, path, data):
        """Cache directory listing"""
        with self.lock:
            self.dir_cache[path] = {
                'data': data,
                'time': time.time()
            }
    
    def get_meta(self, key):
        """Get cached metadata"""
        with self.lock:
            if key in self.meta_cache:
                entry = self.meta_cache[key]
                if time.time() - entry['time'] < self.ttl:
                    return entry['data']
                else:
                    del self.meta_cache[key]
        return None
    
    def set_meta(self, key, data):
        """Cache metadata"""
        with self.lock:
            self.meta_cache[key] = {
                'data': data,
                'time': time.time()
            }
    
    def invalidate_dir(self, path):
        """Invalidate specific directory cache"""
        with self.lock:
            if path in self.dir_cache:
                del self.dir_cache[path]
    
    def invalidate_meta(self, key):
        """Invalidate specific metadata"""
        with self.lock:
            if key in self.meta_cache:
                del self.meta_cache[key]
    
    def clear(self):
        """Clear all caches"""
        with self.lock:
            self.dir_cache.clear()
            self.meta_cache.clear()
    
    def cleanup_expired(self):
        """Remove expired entries"""
        now = time.time()
        with self.lock:
            # Clean directory cache
            expired_dirs = [
                k for k, v in self.dir_cache.items()
                if now - v['time'] >= self.ttl
            ]
            for k in expired_dirs:
                del self.dir_cache[k]
            
            # Clean meta cache
            expired_meta = [
                k for k, v in self.meta_cache.items()
                if now - v['time'] >= self.ttl
            ]
            for k in expired_meta:
                del self.meta_cache[k]
            
            return len(expired_dirs) + len(expired_meta)
    
    def get_stats(self):
        """Get cache statistics"""
        with self.lock:
            return {
                'dir_entries': len(self.dir_cache),
                'meta_entries': len(self.meta_cache),
                'total_entries': len(self.dir_cache) + len(self.meta_cache)
            }
