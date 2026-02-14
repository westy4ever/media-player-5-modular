# ============================================================================
# ModernMedia/__init__.py v5.0 - Modular
# ============================================================================

"""
Modern Media Player v5.0
Professional media player for OpenATV set-top boxes

Features:
- 5 instant-apply themes
- Smart resume with validation
- Poster/thumbnail display
- Multi-profile support
- Complete watch history & statistics
- Playlist management
- Series detection
"""

__version__ = "5.0.0"
__author__ = "ModernMedia Team"
__date__ = "2024-12"

# Package exports
from .constants import VERSION, MEDIA_EXTENSIONS, SUBTITLE_EXTENSIONS

__all__ = [
    'VERSION',
    'MEDIA_EXTENSIONS', 
    'SUBTITLE_EXTENSIONS',
]
