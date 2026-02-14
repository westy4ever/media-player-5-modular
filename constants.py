# ============================================================================
# ModernMedia/constants.py v5.0 - Modular Constants
# ============================================================================

import os

# Version
VERSION = "5.2.0"
VERSION_DATE = "2024-12"

# Media file extensions
MEDIA_EXTENSIONS = (
    '.mkv', '.avi', '.mp4', '.ts', '.mov', '.m4v', '.flv', '.mpg', '.mpeg',
    '.vob', '.divx', '.xvid', '.wmv', '.iso', '.dat', '.mk3d', '.m2ts',
    '.mts', '.trp', '.tp', '.webm', '.ogv', '.3gp', '.f4v', '.asf'
)

# Subtitle extensions
SUBTITLE_EXTENSIONS = (
    '.srt', '.sub', '.ass', '.ssa', '.vtt', '.idx', '.sup', '.txt'
)

# Playback settings
MIN_RESUME_TIME = 10        # Minimum seconds to save resume
END_THRESHOLD = 30          # Seconds from end to mark complete
RESUME_SAVE_INTERVAL = 30   # Auto-save interval during playback

# Display settings
MAX_PATH_DISPLAY_LENGTH = 70
MAX_RECENT_FILES = 50
THUMBNAIL_SIZE = (320, 180)
POSTER_SIZE = (280, 420)

# Sort options
SORT_KEYS = {
    "name_asc": ("Name (A-Z)", False),
    "name_desc": ("Name (Z-A)", True),
    "date_asc": ("Date (Oldest)", False),
    "date_desc": ("Date (Newest)", True),
    "size_asc": ("Size (Smallest)", False),
    "size_desc": ("Size (Largest)", True)
}

# Media paths detection
def detect_media_paths():
    """Detect available media mount points"""
    paths = []
    common_paths = [
        "/media/hdd/", 
        "/media/usb/", 
        "/media/sdcard/", 
        "/media/", 
        "/"
    ]
    
    for path in common_paths:
        if os.path.exists(path) and os.access(path, os.R_OK):
            if path not in paths:
                paths.append(path)
    
    # Check for common subdirectories
    movie_subdirs = ["movies", "video", "films", "videos"]
    for base_path in paths[:]:
        for subdir in movie_subdirs:
            sub_path = os.path.join(base_path, subdir, "")
            if os.path.exists(sub_path):
                if sub_path not in paths:
                    paths.append(sub_path)
    
    return paths if paths else ["/media/"]

ALTERNATIVE_PATHS = detect_media_paths()
DEFAULT_START_DIR = ALTERNATIVE_PATHS[0] if ALTERNATIVE_PATHS else "/media/"

# Database paths (priority order)
DB_PATHS = [
    "/hdd/modernmedia_v5.db",
    "/media/hdd/modernmedia_v5.db",
    "/media/usb/modernmedia_v5.db",
    "/tmp/modernmedia_v5.db"
]

# Cache settings
CACHE_TTL = 3600  # 1 hour
CACHE_DIR = "/hdd/.modernmedia_cache"
THUMB_CACHE_DIR = "/hdd/.modernmedia_thumbs"

# Logging
LOG_DIR = "/tmp/modernmedia"
LOG_FILE = os.path.join(LOG_DIR, "plugin.log")

print(f"[ModernMedia] Constants v{VERSION} loaded")
print(f"[ModernMedia] Detected {len(ALTERNATIVE_PATHS)} media paths")
