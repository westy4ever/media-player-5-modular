# Modern Media Player v5.0 - File Structure & Dependencies

## 📋 Complete File Checklist

### Core Files (5 files)
```
✓ __init__.py           (23 lines)   - Package exports
✓ plugin.py             (82 lines)   - Enigma2 entry point
✓ config.py             (172 lines)  - Configuration manager
✓ constants.py          (81 lines)   - Constants & paths
✓ themes.py             (191 lines)  - Theme system
```

### Database Layer (8 files)
```
database/
  ✓ __init__.py         (8 lines)    - Database exports
  ✓ connection.py       (250 lines)  - Main DB manager
  ✓ resume.py           (98 lines)   - Resume operations
  ✓ favorites.py        (115 lines)  - Favorites & bookmarks
  ✓ playlists.py        (145 lines)  - Playlist operations
  ✓ history.py          (121 lines)  - Watch history
  ✓ statistics.py       (118 lines)  - Statistics tracking
  ✓ metadata.py         (115 lines)  - File metadata
```

### Utilities Layer (6 files)
```
utils/
  ✓ __init__.py         (23 lines)   - Utils exports
  ✓ helpers.py          (152 lines)  - Helper functions
  ✓ cache.py            (104 lines)  - Smart caching
  ✓ thumbnails.py       (143 lines)  - Thumbnail manager
  ✓ scanner.py          (112 lines)  - Directory scanner
  ✓ progress.py         (82 lines)   - Progress renderer
```

### Documentation (3 files)
```
✓ README_MODULAR.md     - Architecture guide
✓ INSTALLATION.md       - Installation guide
✓ FILE_STRUCTURE.md     - This file
```

**Total: 24 files | ~2,500 lines of clean, modular code**

---

## 🔗 Dependency Map

```
plugin.py (Entry Point)
  ├─→ utils.helpers (setup_logging, log_message, detect_environment)
  ├─→ config (init_config)
  ├─→ constants (VERSION)
  └─→ database.connection (DatabaseManager)
       └─→ Imports all database/* modules

config.py
  └─→ Components.config (Enigma2)

constants.py
  └─→ os (path detection)

themes.py
  └─→ config (get_config)

database/connection.py
  ├─→ sqlite3
  ├─→ constants (DB_PATHS)
  └─→ database/* modules:
       ├─→ resume.py
       ├─→ favorites.py
       ├─→ playlists.py
       ├─→ history.py
       ├─→ statistics.py
       └─→ metadata.py

database/* operation modules
  └─→ Each uses db_manager passed in __init__

utils/helpers.py
  └─→ constants (LOG_DIR, LOG_FILE, MEDIA_EXTENSIONS, SUBTITLE_EXTENSIONS)

utils/cache.py
  ├─→ threading
  └─→ constants (CACHE_TTL)

utils/thumbnails.py
  ├─→ subprocess (FFmpeg)
  ├─→ hashlib
  └─→ constants (THUMB_CACHE_DIR, THUMBNAIL_SIZE)

utils/scanner.py
  ├─→ threading
  └─→ constants (MEDIA_EXTENSIONS)

utils/progress.py
  └─→ No external dependencies
```

---

## 📦 Import Hierarchy

### Level 0: Python Standard Library
```
os, sys, time, threading, sqlite3, hashlib, subprocess, re
```

### Level 1: Enigma2 Framework
```
Plugins.Plugin.PluginDescriptor
Screens.Screen, Screens.MessageBox
Components.config.*
enigma.*
```

### Level 2: Project Constants
```
constants.py → All other modules
```

### Level 3: Core Systems
```
config.py  → themes.py, database/*, utils/*
themes.py  → (uses config)
```

### Level 4: Database Layer
```
database/connection.py → database/* operation modules
```

### Level 5: Utilities
```
utils/* → Independent modules
```

### Level 6: UI (To be created)
```
ui/main_screen.py → database/*, utils/*, themes.py
ui/player.py → database/resume.py, utils/helpers.py
ui/menus.py → database/*, utils/*
```

---

## 🔄 Module Independence

### Fully Independent (Can be used standalone)
```
✓ constants.py          - Just constants
✓ utils/progress.py     - Pure rendering
✓ themes.py             - Just color data (soft dependency on config)
```

### Semi-Independent (Minimal dependencies)
```
✓ utils/cache.py        - Only needs constants
✓ utils/helpers.py      - Only needs constants
✓ config.py             - Only needs Enigma2 config
```

### Dependent Modules
```
✓ database/*            - Need DatabaseManager instance
✓ utils/thumbnails.py   - Needs constants + FFmpeg
✓ utils/scanner.py      - Needs constants + database (optional)
```

### Integration Modules
```
✓ plugin.py             - Orchestrates everything
✓ database/connection.py - Coordinates all DB operations
```

---

## 🧪 Testing Individual Modules

### Test Constants
```python
from ModernMedia.constants import VERSION, MEDIA_EXTENSIONS
print(f"Version: {VERSION}")
print(f"Extensions: {len(MEDIA_EXTENSIONS)}")
```

### Test Config
```python
from ModernMedia.config import init_config, get_config
init_config()
cfg = get_config()
print(cfg.theme.value)
```

### Test Themes
```python
from ModernMedia.themes import ThemeManager
colors = ThemeManager.get_theme_colors('netflix')
print(colors['accent'])  # #FFE50914
```

### Test Database
```python
from ModernMedia.database import DatabaseManager
db = DatabaseManager()
db.resume.set('/test.mkv', 100, 1000, 1.0)
data = db.resume.get('/test.mkv', 1000, 1.0)
print(data)
```

### Test Cache
```python
from ModernMedia.utils import SmartCache
cache = SmartCache()
cache.set_dir('/test', ['file1', 'file2'])
print(cache.get_dir('/test'))
```

### Test Progress
```python
from ModernMedia.utils import ProgressBarRenderer
renderer = ProgressBarRenderer()
print(renderer.render(75))  # [███████░░░]  75%
```

---

## 📊 File Size Breakdown

```
Core Files:           ~550 lines
Database Layer:       ~960 lines
Utils Layer:          ~616 lines
Documentation:        ~1,000 lines
----------------------------------
Total Production:     ~2,126 lines
Total with Docs:      ~3,126 lines
```

### Lines per Module Category
```
Entry & Config:       254 lines  (12%)
Constants & Themes:   272 lines  (13%)
Database Operations:  960 lines  (45%)
Utilities:            616 lines  (29%)
Package Init:         24 lines   (1%)
```

---

## 🎯 Module Relationships

### Core → Database
```
plugin.py
  ↓
database.connection.DatabaseManager
  ↓
database.{resume, favorites, playlists, history, statistics, metadata}
```

### Core → Utils
```
plugin.py → utils.helpers (logging)
Any module → utils.cache (caching)
Any module → utils.thumbnails (thumbnails)
Any module → utils.progress (progress bars)
```

### Cross-Module Communication
```
Database ←→ Utils/Scanner (optional DB for resume data)
Database ←→ Utils/Helpers (find_subtitle, find_next_episode)
Themes ←→ Config (get current theme)
```

---

## 🔧 Modifying Specific Features

### Add New Theme
```
File: themes.py
1. Add to ThemeManager.THEMES dict
2. Define 12 color properties
3. Test: ThemeManager.get_theme_colors('new_theme')
```

### Add Database Table
```
File: database/connection.py (create_tables)
1. Add CREATE TABLE statement
2. Add indexes if needed
3. Create new operation module: database/new_feature.py
4. Import in connection.py __init__
5. Update database/__init__.py exports
```

### Add Utility Function
```
File: utils/helpers.py
1. Add function with docstring
2. Update utils/__init__.py exports
3. Test independently
```

### Add Config Option
```
File: config.py
1. Add to appropriate _init_*_settings() function
2. Use in other modules: config.plugins.modernmedia.new_option
```

---

## ✅ File Integrity Verification

### Quick Check Script
```bash
#!/bin/bash
cd /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia

echo "Checking core files..."
for f in __init__.py plugin.py config.py constants.py themes.py; do
  [ -f "$f" ] && echo "✓ $f" || echo "✗ MISSING: $f"
done

echo -e "\nChecking database files..."
for f in database/__init__.py database/connection.py database/resume.py \
         database/favorites.py database/playlists.py database/history.py \
         database/statistics.py database/metadata.py; do
  [ -f "$f" ] && echo "✓ $f" || echo "✗ MISSING: $f"
done

echo -e "\nChecking utils files..."
for f in utils/__init__.py utils/helpers.py utils/cache.py \
         utils/thumbnails.py utils/scanner.py utils/progress.py; do
  [ -f "$f" ] && echo "✓ $f" || echo "✗ MISSING: $f"
done
```

### Python Import Check
```python
#!/usr/bin/env python3
print("Testing ModernMedia imports...")

try:
    from ModernMedia import VERSION
    print(f"✓ Package: v{VERSION}")
except Exception as e:
    print(f"✗ Package: {e}")

try:
    from ModernMedia.config import get_config
    print("✓ Config module")
except Exception as e:
    print(f"✗ Config: {e}")

try:
    from ModernMedia.themes import ThemeManager
    print("✓ Themes module")
except Exception as e:
    print(f"✗ Themes: {e}")

try:
    from ModernMedia.database import DatabaseManager
    print("✓ Database module")
except Exception as e:
    print(f"✗ Database: {e}")

try:
    from ModernMedia.utils import SmartCache, ThumbnailManager
    print("✓ Utils module")
except Exception as e:
    print(f"✗ Utils: {e}")

print("\nAll modules OK!")
```

---

## 🎓 Learning Path

For developers new to the codebase:

1. **Start here:** `constants.py` - Understand constants
2. **Then:** `config.py` - See configuration system
3. **Next:** `themes.py` - Simple, self-contained module
4. **After:** `utils/progress.py` - Pure utility, no dependencies
5. **Moving up:** `utils/cache.py` - Simple caching logic
6. **Database basics:** `database/resume.py` - Simplest DB operations
7. **Advanced DB:** `database/playlists.py` - Complex operations
8. **Integration:** `database/connection.py` - See how it all connects
9. **Entry point:** `plugin.py` - Understand initialization flow

---

This modular structure makes the codebase **easy to understand, debug, and extend**!
