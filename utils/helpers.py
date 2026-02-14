# ============================================================================
# ModernMedia/utils/helpers.py v5.0 - Helper Functions
# ============================================================================

import sys
import os
import time
from ..constants import LOG_DIR, LOG_FILE

def setup_logging():
    """Setup logging directory"""
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR, exist_ok=True)
        return True
    except:
        return False

def log_message(message):
    """Log message to file and console"""
    try:
        if setup_logging():
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] {message}\n")
        print(f"[ModernMedia] {message}")
    except:
        print(f"[ModernMedia] {message}")

def detect_environment():
    """Detect system environment"""
    info = {
        'python_version': sys.version.split()[0],
        'platform': sys.platform,
        'image': 'Unknown'
    }
    
    try:
        from boxbranding import getImageVersion, getImageDistro
        info['image'] = f"{getImageDistro()} {getImageVersion()}"
    except:
        try:
            if os.path.exists("/etc/image-version"):
                with open("/etc/image-version", "r", encoding="utf-8") as f:
                    info['image'] = f.read().strip()
        except:
            pass
    
    return info

def format_size(bytes_size):
    """Format file size"""
    if bytes_size >= 1024**3:
        return f"{bytes_size / (1024**3):.2f} GB"
    elif bytes_size >= 1024**2:
        return f"{bytes_size / (1024**2):.1f} MB"
    elif bytes_size >= 1024:
        return f"{bytes_size / 1024:.1f} KB"
    else:
        return f"{bytes_size} B"

def format_time(seconds):
    """Format time in seconds to readable string"""
    if seconds < 60:
        return f"{int(seconds)}s"
    
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    
    if mins < 60:
        return f"{mins}:{secs:02d}"
    
    hours = mins // 60
    mins = mins % 60
    return f"{hours}:{mins:02d}:{secs:02d}"

def truncate_path(path, max_length=70):
    """Truncate path for display"""
    if len(path) <= max_length:
        return path
    
    parts = [p for p in path.split(os.sep) if p]
    if len(parts) > 2:
        return f".../{'/'.join(parts[-2:])}"
    return path

def detect_series_pattern(filename):
    """Detect series naming pattern (S01E02 or 1x02)"""
    import re
    pattern = re.compile(r'[Ss](\d+)[Ee](\d+)|(\d+)x(\d+)')
    match = pattern.search(filename)
    
    if match:
        season = int(match.group(1) or match.group(3))
        episode = int(match.group(2) or match.group(4))
        return season, episode
    
    return None, None

def find_next_episode(current_file, directory):
    """Find next episode in series"""
    import re
    from ..constants import MEDIA_EXTENSIONS
    
    current_name = os.path.basename(current_file)
    season, episode = detect_series_pattern(current_name)
    
    if season is None or episode is None:
        return None
    
    next_episode = episode + 1
    pattern = re.compile(r'[Ss](\d+)[Ee](\d+)|(\d+)x(\d+)')
    
    try:
        for file in os.listdir(directory):
            if not file.lower().endswith(MEDIA_EXTENSIONS):
                continue
            
            match = pattern.search(file)
            if match:
                file_season = int(match.group(1) or match.group(3))
                file_episode = int(match.group(2) or match.group(4))
                
                if file_season == season and file_episode == next_episode:
                    return os.path.join(directory, file)
    except:
        pass
    
    return None

def find_subtitle(video_path):
    """Find matching subtitle file"""
    from ..constants import SUBTITLE_EXTENSIONS
    
    base = os.path.splitext(video_path)[0]
    for ext in SUBTITLE_EXTENSIONS:
        sub_path = base + ext
        if os.path.exists(sub_path):
            return sub_path
    
    return None
