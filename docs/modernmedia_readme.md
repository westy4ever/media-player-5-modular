# Modern Media Player v5.0 - Modular Architecture

## 📁 Project Structure

```
ModernMedia/
├── __init__.py                 # Package initialization
├── plugin.py                   # Entry point for Enigma2
├── config.py                   # Configuration management
├── constants.py                # Constants and settings
├── themes.py                   # Theme system (5 themes)
│
├── database/                   # Database layer (SQLite)
│   ├── __init__.py
│   ├── connection.py          # Main DB manager
│   ├── resume.py              # Resume points
│   ├── favorites.py           # Favorites & bookmarks
│   ├── playlists.py           # Playlist management
│   ├── history.py             # Watch history & recent
│   ├── statistics.py          # Viewing statistics
│   └── metadata.py            # File metadata
│
├── ui/                         # UI layer (to be created)
│   ├── __init__.py
│   ├── main_screen.py         # Main browser screen
│   ├── player.py              # Video player
│   ├── menus.py               # Menu handlers
│   └── widgets.py             # Custom widgets
│
└── utils/                      # Utilities
    ├── __init__.py
    ├── helpers.py             # Helper functions
    ├── cache.py               # Smart caching
    ├── thumbnails.py          # Thumbnail manager
    ├── scanner.py             # Directory scanner
    └── progress.py            # Progress bars
```

---

## 🔧 Module Responsibilities

### **Core Modules**

#### `plugin.py` - Entry Point
- Plugin registration
- Main initialization
- Error handling & logging
- Component loading

#### `config.py` - Configuration
- Settings initialization
- Config categories:
  - Basic settings (paths, sorting)
  - View settings (theme, display)
  - Playback settings (resume, subtitles)
  - Database settings (cleanup, history)
  - Profile settings
  - Advanced settings

#### `constants.py` - Constants
- File extensions (24 video, 8 subtitle)
- Paths detection
- Display constants
- Playback thresholds
- Database paths

#### `themes.py` - Theme System
- 5 themes: dark, light, blue, netflix, plex
- Instant theme switching
- Color scheme management
- Theme validation

---

### **Database Layer** (`database/`)

#### `connection.py` - DatabaseManager
Central manager that:
- Establishes SQLite connection
- Creates all tables
- Provides thread-safe access
- Imports all operation modules
- Exposes: `db.resume`, `db.favorites`, `db.playlists`, etc.

#### `resume.py` - ResumeOperations
```python
db.resume.get(file_path, size, mtime)      # Get with validation
db.resume.set(file_path, position, ...)    # Save position
db.resume.delete(file_path)                 # Clear resume
db.resume.cleanup_old(days=30)              # Maintenance
```

#### `favorites.py` - FavoritesOperations
```python
db.favorites.add(file_path, profile)
db.favorites.remove(file_path)
db.favorites.is_favorite(file_path)
db.favorites.get_all(profile, limit)
db.favorites.toggle(file_path)
db.favorites.add_bookmark(dir_path, name)   # Directories
db.favorites.get_bookmarks(profile)
```

#### `playlists.py` - PlaylistOperations
```python
db.playlists.create(name, profile)
db.playlists.delete(playlist_id)
db.playlists.get_all(profile)
db.playlists.add_item(playlist_id, file_path)
db.playlists.get_items(playlist_id)
db.playlists.reorder_items(playlist_id, paths)
```

#### `history.py` - HistoryOperations
```python
# Recent files
db.history.add_recent(file_path, profile)
db.history.get_recent(profile, limit)

# Watch history
db.history.add_watch(file_path, duration)
db.history.get_watch_history(profile, limit)
db.history.get_file_history(file_path)
```

#### `statistics.py` - StatisticsOperations
```python
db.statistics.record_view(file, duration, profile)
db.statistics.get_stats(profile, days)
db.statistics.get_daily_stats(profile, days)
db.statistics.get_most_watched(profile, limit)
```

#### `metadata.py` - MetadataOperations
```python
db.metadata.set(file_path, {title, year, genre, ...})
db.metadata.get(file_path)
db.metadata.search(query)
db.metadata.get_by_genre(genre)
db.metadata.get_by_year(year)
```

---

### **Utilities Layer** (`utils/`)

#### `helpers.py`
```python
setup_logging()                    # Setup log directory
log_message(msg)                   # Log to file + console
detect_environment()               # System info
format_size(bytes)                 # Human-readable size
format_time(seconds)               # Time formatting
detect_series_pattern(filename)    # S01E02 detection
find_next_episode(file, dir)       # Auto-play next
find_subtitle(video_path)          # Subtitle matching
```

#### `cache.py` - SmartCache
```python
cache = SmartCache(ttl=3600)
cache.get_dir(path)               # Get cached directory
cache.set_dir(path, data)         # Cache directory
cache.clear()                      # Clear all
cache.cleanup_expired()            # Maintenance
```

#### `thumbnails.py` - ThumbnailManager
```python
thumb_mgr = ThumbnailManager()
thumb_mgr.has_thumb(video_path)
thumb_mgr.generate(video_path, timestamp=60)
thumb_mgr.batch_generate(paths, callback)
thumb_mgr.get_cache_size()
thumb_mgr.clear_cache()
```

#### `scanner.py` - DirectoryScanner
```python
scanner = DirectoryScanner(path, db, media_ext, search, cache)
scanner.start()                    # Start threaded scan
scanner.is_alive()                 # Check if running
scanner.stop()                     # Stop scanning
results = scanner.results          # Get results
```

#### `progress.py` - ProgressBarRenderer
```python
renderer = ProgressBarRenderer()
renderer.render(percentage, length=10)     # [████░░░░░░] 40%
renderer.render_mini(percentage)           # 5-char bar
renderer.get_color(percentage)             # Color hint
```

---

## 🚀 Usage Examples

### Example 1: Database Operations
```python
from ModernMedia.database import DatabaseManager

# Initialize
db = DatabaseManager()

# Resume operations
db.resume.set('/media/movie.mkv', 1234, 5000000, 1234567890)
resume_data = db.resume.get('/media/movie.mkv', 5000000, 1234567890)

# Favorites
db.favorites.add('/media/movie.mkv')
if db.favorites.is_favorite('/media/movie.mkv'):
    print("Is favorite!")

# Statistics
db.statistics.record_view('/media/movie.mkv', 120, 'default')
stats = db.statistics.get_stats('default', days=30)
print(f"Watched {stats['total_files']} files")
```

### Example 2: Utilities
```python
from ModernMedia.utils import SmartCache, ThumbnailManager

# Caching
cache = SmartCache()
cache.set_dir('/media/movies', file_list)
cached = cache.get_dir('/media/movies')

# Thumbnails
thumb_mgr = ThumbnailManager()
thumb_path = thumb_mgr.generate('/media/movie.mkv')
```

### Example 3: Theme Switching
```python
from ModernMedia.themes import ThemeManager

# Get current theme colors
colors = ThemeManager.get_theme_colors('netflix')
print(colors['accent'])  # #FFE50914

# Cycle theme
next_theme = ThemeManager.cycle_theme()
```

---

## 🐛 Debugging Guide

### Enable Debug Mode
```python
from ModernMedia.config import get_config
cfg = get_config()
cfg.debug_mode.value = True
cfg.debug_mode.save()
```

### Check Logs
```bash
tail -f /tmp/modernmedia/plugin.log
```

### Test Database
```python
from ModernMedia.database import DatabaseManager
db = DatabaseManager()

# Check connection
print(f"DB Size: {db.get_size_mb():.2f} MB")

# Test resume
db.resume.set('/test.mkv', 100, 1000, 1.0)
data = db.resume.get('/test.mkv', 1000, 1.0)
print(data)

# Optimize
db.optimize()
db.vacuum()
```

### Test Cache
```python
from ModernMedia.utils import SmartCache
cache = SmartCache()

# Test cache
cache.set_dir('/media', ['file1', 'file2'])
cached = cache.get_dir('/media')
print(cached)

# Stats
stats = cache.get_stats()
print(f"Cached: {stats['total_entries']} entries")
```

---

## 🔄 Update Workflow

### Updating Database Schema
1. Edit `database/connection.py` - add table
2. Update relevant operation module
3. Test with `db.optimize()`

### Adding New Feature
1. Identify layer (database/ui/utils)
2. Create/update module
3. Add to `__init__.py` exports
4. Update `plugin.py` if needed
5. Test independently

### Modifying Theme
1. Edit `themes.py`
2. Add/modify theme in `THEMES` dict
3. Update `get_theme_choices()`
4. Test instant switching

---

## ✅ Benefits of Modular Design

1. **Easy Debugging** - Isolate issues to specific modules
2. **Independent Testing** - Test each module separately
3. **Clear Responsibilities** - Each file has one purpose
4. **Scalability** - Add features without breaking existing code
5. **Team Development** - Multiple developers can work simultaneously
6. **Maintainability** - Changes localized to relevant modules
7. **Code Reuse** - Import only what you need
8. **Performance** - Load modules on-demand

---

## 📝 Development Checklist

When adding a new feature:
- [ ] Identify the correct module
- [ ] Add function/class to module
- [ ] Update `__init__.py` exports
- [ ] Add docstrings
- [ ] Test independently
- [ ] Update this README
- [ ] Add example usage
- [ ] Test integration

---

## 🎯 Next Steps (UI Layer - To Be Created)

The UI layer needs to be modularized similarly:
- `ui/main_screen.py` - Browser with file list
- `ui/player.py` - Video playback
- `ui/menus.py` - All menu handlers
- `ui/widgets.py` - Reusable widgets
- `ui/skins.py` - Skin generation

This will complete the full modular architecture.
