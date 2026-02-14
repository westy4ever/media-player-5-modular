# ============================================================================
# ModernMedia/config.py v5.1 - Fixed Configuration
# ============================================================================

from Components.config import (
    config, ConfigSubsection, ConfigDirectory, ConfigSelection,
    ConfigYesNo, ConfigInteger, ConfigText
)

def init_config():
    """Initialize all configuration options"""
    try:
        print("[ModernMedia] Initializing configuration...")
        
        if not hasattr(config.plugins, 'modernmedia'):
            config.plugins.modernmedia = ConfigSubsection()
        
        _init_basic_settings()
        _init_view_settings()
        _init_playback_settings()
        _init_database_settings()
        _init_profile_settings()
        _init_advanced_settings()
        
        print("[ModernMedia] Configuration initialized ✓")
        return True
        
    except Exception as e:
        print(f"[ModernMedia] Config error: {e}")
        return False

def _init_basic_settings():
    """Basic navigation settings"""
    cfg = config.plugins.modernmedia
    
    if not hasattr(cfg, 'start_dir'):
        cfg.start_dir = ConfigDirectory(default="/media/")
    
    if not hasattr(cfg, 'sort_key'):
        cfg.sort_key = ConfigSelection(default="name_asc", choices=[
            ("name_asc", "Name (A-Z)"),
            ("name_desc", "Name (Z-A)"),
            ("date_asc", "Date (Oldest)"),
            ("date_desc", "Date (Newest)"),
            ("size_asc", "Size (Smallest)"),
            ("size_desc", "Size (Largest)")
        ])
    
    if not hasattr(cfg, 'default_resume_action'):
        cfg.default_resume_action = ConfigSelection(default="ask", choices=[
            ("ask", "Ask every time"),
            ("start", "Always start from beginning"),
            ("resume", "Always resume playback")
        ])

def _init_view_settings():
    """Visual display settings"""
    cfg = config.plugins.modernmedia
    
    if not hasattr(cfg, 'view_mode'):
        cfg.view_mode = ConfigSelection(default="list", choices=[
            ("list", "List View"),
            ("details", "Details View"),
            ("grid", "Grid View")
        ])
    
    if not hasattr(cfg, 'show_thumbnails'):
        cfg.show_thumbnails = ConfigYesNo(default=False)
    
    # FIXED: Progress bars now enabled by default and more visible
    if not hasattr(cfg, 'show_progress_bars'):
        cfg.show_progress_bars = ConfigYesNo(default=True)
    
    if not hasattr(cfg, 'show_resume_icons'):
        cfg.show_resume_icons = ConfigYesNo(default=True)
    
    # REMOVED: No theme setting - themes disabled
    
    if not hasattr(cfg, 'show_animations'):
        cfg.show_animations = ConfigYesNo(default=False)  # Disabled by default

def _init_playback_settings():
    """Playback behavior settings"""
    cfg = config.plugins.modernmedia
    
    # FIXED: Auto-play next disabled by default
    if not hasattr(cfg, 'auto_play_next'):
        cfg.auto_play_next = ConfigYesNo(default=False)
    
    if not hasattr(cfg, 'detect_series'):
        cfg.detect_series = ConfigYesNo(default=True)
    
    if not hasattr(cfg, 'auto_load_subtitles'):
        cfg.auto_load_subtitles = ConfigYesNo(default=True)
    
    if not hasattr(cfg, 'small_skip_seconds'):
        cfg.small_skip_seconds = ConfigInteger(default=10, limits=(5, 60))
    
    if not hasattr(cfg, 'large_skip_seconds'):
        cfg.large_skip_seconds = ConfigInteger(default=60, limits=(30, 600))

def _init_database_settings():
    """Database maintenance settings"""
    cfg = config.plugins.modernmedia
    
    if not hasattr(cfg, 'auto_cleanup_days'):
        cfg.auto_cleanup_days = ConfigInteger(default=30, limits=(0, 365))
    
    if not hasattr(cfg, 'max_recent_files'):
        cfg.max_recent_files = ConfigInteger(default=50, limits=(10, 200))
    
    if not hasattr(cfg, 'enable_watch_history'):
        cfg.enable_watch_history = ConfigYesNo(default=True)

def _init_profile_settings():
    """User profile settings"""
    cfg = config.plugins.modernmedia
    
    if not hasattr(cfg, 'enable_profiles'):
        cfg.enable_profiles = ConfigYesNo(default=False)
    
    if not hasattr(cfg, 'current_profile'):
        cfg.current_profile = ConfigText(default="default")

def _init_advanced_settings():
    """Advanced features"""
    cfg = config.plugins.modernmedia
    
    if not hasattr(cfg, 'scan_subdirs'):
        cfg.scan_subdirs = ConfigYesNo(default=False)
    
    if not hasattr(cfg, 'cache_directory_listings'):
        cfg.cache_directory_listings = ConfigYesNo(default=True)
    
    if not hasattr(cfg, 'debug_mode'):
        cfg.debug_mode = ConfigYesNo(default=False)

def get_config():
    """Get config object"""
    return config.plugins.modernmedia

# Auto-initialize on import
try:
    init_config()
except Exception as e:
    print(f"[ModernMedia] Config auto-init failed: {e}")
