# ============================================================================
# ModernMedia/utils/thumbnails.py v5.0 - Thumbnail Manager
# ============================================================================

import os
import hashlib
import subprocess
import threading
from ..constants import THUMB_CACHE_DIR, THUMBNAIL_SIZE

class ThumbnailManager:
    """
    Thumbnail generation and caching
    Uses FFmpeg to extract video frames
    """
    
    def __init__(self, cache_dir=THUMB_CACHE_DIR):
        self.cache_dir = cache_dir
        self.generating = set()
        self.lock = threading.RLock()
        self.setup_cache()
    
    def setup_cache(self):
        """Setup cache directory"""
        try:
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir, exist_ok=True)
            print(f"[Thumbs] Cache: {self.cache_dir}")
        except:
            # Fallback to /tmp
            self.cache_dir = "/tmp/.modernmedia_thumbs"
            os.makedirs(self.cache_dir, exist_ok=True)
            print(f"[Thumbs] Fallback: {self.cache_dir}")
    
    def get_thumb_path(self, video_path):
        """Get thumbnail path for video"""
        path_hash = hashlib.md5(video_path.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{path_hash}.jpg")
    
    def has_thumb(self, video_path):
        """Check if thumbnail exists"""
        return os.path.exists(self.get_thumb_path(video_path))
    
    def generate(self, video_path, timestamp=60):
        """Generate thumbnail using FFmpeg"""
        thumb_path = self.get_thumb_path(video_path)
        
        # Already exists
        if os.path.exists(thumb_path):
            return thumb_path
        
        # Check if already generating
        with self.lock:
            if video_path in self.generating:
                return None
            self.generating.add(video_path)
        
        try:
            width, height = THUMBNAIL_SIZE
            cmd = [
                'ffmpeg',
                '-ss', str(timestamp),
                '-i', video_path,
                '-vframes', '1',
                '-s', f'{width}x{height}',
                '-q:v', '2',
                thumb_path,
                '-y'
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(thumb_path):
                print(f"[Thumbs] Generated: {os.path.basename(video_path)}")
                return thumb_path
        
        except Exception as e:
            print(f"[Thumbs] Error: {e}")
        
        finally:
            with self.lock:
                self.generating.discard(video_path)
        
        return None
    
    def batch_generate(self, video_paths, progress_callback=None):
        """Generate thumbnails for multiple videos"""
        total = len(video_paths)
        generated = 0
        
        for idx, path in enumerate(video_paths):
            if self.has_thumb(path):
                continue
            
            if self.generate(path):
                generated += 1
            
            if progress_callback:
                progress_callback(idx + 1, total, generated)
        
        return generated
    
    def delete_thumb(self, video_path):
        """Delete thumbnail for video"""
        thumb_path = self.get_thumb_path(video_path)
        try:
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
                return True
        except:
            pass
        return False
    
    def clear_cache(self):
        """Clear all thumbnails"""
        try:
            for file in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return True
        except:
            return False
    
    def get_cache_size(self):
        """Get total cache size in bytes"""
        try:
            total = 0
            for file in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, file)
                if os.path.isfile(file_path):
                    total += os.path.getsize(file_path)
            return total
        except:
            return 0
    
    def get_cache_count(self):
        """Get number of cached thumbnails"""
        try:
            return len([f for f in os.listdir(self.cache_dir) if f.endswith('.jpg')])
        except:
            return 0
