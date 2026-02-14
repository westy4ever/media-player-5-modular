# Modern Media Player v5.0 - Installation Guide

## 📦 Package Contents

### ✅ Complete Modular File List

```
ModernMedia/
├── __init__.py                 ✓ Package init
├── plugin.py                   ✓ Plugin entry point
├── config.py                   ✓ Configuration system
├── constants.py                ✓ Constants & paths
├── themes.py                   ✓ Theme manager (5 themes)
│
├── database/                   ✓ 8 modules
│   ├── __init__.py
│   ├── connection.py
│   ├── resume.py
│   ├── favorites.py
│   ├── playlists.py
│   ├── history.py
│   ├── statistics.py
│   └── metadata.py
│
├── utils/                      ✓ 6 modules
│   ├── __init__.py
│   ├── helpers.py
│   ├── cache.py
│   ├── thumbnails.py
│   ├── scanner.py
│   └── progress.py
│
├── ui/                         ✓ 5 modules
│   ├── __init__.py
│   ├── skins.py
│   ├── main_screen.py
│   ├── player.py
│   └── menus.py
│
└── docs/
    ├── README_MODULAR.md
    ├── INSTALLATION.md
    ├── FILE_STRUCTURE.md
    └── UI_LAYER_COMPLETE.md

Total: 28 modular files
```

**Note:** The following old monolithic files are REPLACED by the modular architecture and should NOT be copied:
- ❌ `ModernMediaScreen.py` → Replaced by `ui/` modules
- ❌ `ModernMediaDB.py` → Replaced by `database/` modules  
- ❌ `ModernMediaThemes.py` → Replaced by `themes.py`
- ❌ `ModernMediaConfig.py` → Replaced by `config.py`
- ❌ `ModernMediaConstants.py` → Replaced by `constants.py`

**Only copy the new modular files listed above.**

---

## 🚀 Installation Steps

### Method 1: Fresh Installation

1. **Create plugin directory:**
   ```bash
   mkdir -p /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia
   ```

2. **Copy all files:**
   ```bash
   # Copy main files
   cp __init__.py plugin.py config.py constants.py themes.py \
      /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/
   
   # Copy database modules
   mkdir -p /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/database
   cp database/*.py \
      /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/database/
   
   # Copy utils modules
   mkdir -p /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/utils
   cp utils/*.py \
      /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/utils/
   
   # Copy UI modules
   mkdir -p /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/ui
   cp ui/*.py \
      /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/ui/
   ```

3. **Set permissions:**
   ```bash
   chmod -R 755 /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia
   ```

4. **Restart Enigma2:**
   ```bash
   killall -9 enigma2
   # Or use GUI: Menu → Restart GUI
   ```

### Method 2: FTP/SCP Upload

1. Connect to receiver via FTP/SCP
2. Navigate to: `/usr/lib/enigma2/python/Plugins/Extensions/`
3. Create folder: `ModernMedia/`
4. Upload all files maintaining directory structure
5. Restart GUI

### Method 3: Using USB

1. Copy `ModernMedia/` folder to USB
2. On receiver:
   ```bash
   cd /media/usb
   cp -r ModernMedia /usr/lib/enigma2/python/Plugins/Extensions/
   ```
3. Restart GUI

---

## 🔍 Verification

### Check Installation
```bash
# List files
ls -la /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/

# Check database module
ls -la /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/database/

# Check utils module
ls -la /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/utils/

# Check UI module
ls -la /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia/ui/
```

### Test Import
```python
# SSH into receiver
python3

>>> from Plugins.Extensions.ModernMedia.config import init_config
>>> init_config()
[ModernMedia] Initializing configuration...
[ModernMedia] Configuration initialized ✓
True

>>> from Plugins.Extensions.ModernMedia.database import DatabaseManager
>>> db = DatabaseManager()
[DB] Using: /hdd/modernmedia_v5.db
[DB] Connected: /hdd/modernmedia_v5.db
[DB] Tables created ✓

>>> from Plugins.Extensions.ModernMedia.ui import ModernMediaScreen
>>> print("UI modules OK")
UI modules OK

>>> print(f"DB Size: {db.get_size_mb():.2f} MB")
DB Size: 0.05 MB
```

### Check Plugin Menu
1. Press `Menu` on remote
2. Navigate to `Plugins` → `Extensions`
3. Look for `Modern Media Player v5.0`
4. Description should say: "Modular architecture - All 36+ features"

---

## 🔧 Configuration

### First Run
On first launch, the plugin will:
1. Create config file: `/etc/enigma2/settings`
2. Create database: `/hdd/modernmedia_v5.db` (or `/tmp/` if no HDD)
3. Create thumbnail cache: `/hdd/.modernmedia_thumbs/`
4. Create log file: `/tmp/modernmedia/plugin.log`

### Check Logs
```bash
# Real-time log
tail -f /tmp/modernmedia/plugin.log

# View full log
cat /tmp/modernmedia/plugin.log

# Check errors
grep ERROR /tmp/modernmedia/plugin.log
```

### Check Database
```bash
# Check if created
ls -lh /hdd/modernmedia_v5.db

# Check size
du -h /hdd/modernmedia_v5.db

# Access with sqlite3
sqlite3 /hdd/modernmedia_v5.db
sqlite> .tables
sqlite> SELECT COUNT(*) FROM resume_points;
sqlite> .quit
```

---

## ⚙️ Post-Installation

### Configure Settings
Press `Blue` button or `Menu` in player to access:
- Start directory
- Theme selection (press `7` to cycle)
- Resume behavior
- View mode
- Animation settings
- Auto-play next episode
- Database cleanup days

### Generate Thumbnails
1. Navigate to a folder with videos
2. Press `0` (zero) to batch generate thumbnails
3. Wait for completion
4. Thumbnails cached in `/hdd/.modernmedia_thumbs/`

### Import Existing Resume Points
If upgrading from old version:
```python
# Example migration script
from ModernMedia.database import DatabaseManager
db = DatabaseManager()

# Your old resume points
old_resumes = [
    ('/media/movie1.mkv', 1234),
    ('/media/movie2.mkv', 5678),
]

for path, position in old_resumes:
    import os
    stats = os.stat(path)
    db.resume.set(path, position, stats.st_size, stats.st_mtime)
```

---

## 🐛 Troubleshooting

### Plugin Not Showing
1. Check file permissions: `chmod -R 755 /usr/lib/.../ModernMedia`
2. Check `plugin.py` exists
3. Restart GUI (not just reboot)
4. Check log: `grep ERROR /tmp/modernmedia/plugin.log`

### Database Errors
```bash
# Check database path
ls -lh /hdd/modernmedia_v5.db

# Check write permissions
touch /hdd/test_write && rm /hdd/test_write

# Rebuild database
rm /hdd/modernmedia_v5.db
# Restart plugin - will recreate
```

### Theme Not Applying
- Press `7` to cycle themes
- Check config: `Settings` → Theme selection
- Themes apply instantly without restart

### Missing Thumbnails
```bash
# Check FFmpeg installed
which ffmpeg

# Install if missing (OpenATV)
opkg update
opkg install ffmpeg

# Manual thumbnail generation
ffmpeg -ss 60 -i /media/movie.mkv -vframes 1 -s 320x180 /tmp/test.jpg
```

### Import Errors
```python
# Check Python version
python3 --version  # Should be 3.9+

# Test imports
python3 -c "from ModernMedia.database import DatabaseManager; print('OK')"
python3 -c "from ModernMedia.utils import SmartCache; print('OK')"
```

---

## 📊 Performance Optimization

### Database Optimization
Run periodically:
```python
from ModernMedia.database import DatabaseManager
db = DatabaseManager()
db.optimize()  # Analyze and optimize
db.vacuum()    # Reclaim space
```

### Cache Management
```python
from ModernMedia.utils import SmartCache, ThumbnailManager

# Clear caches
cache = SmartCache()
cache.clear()

thumb_mgr = ThumbnailManager()
print(f"Cache size: {thumb_mgr.get_cache_size() / 1024**2:.2f} MB")
thumb_mgr.clear_cache()  # If too large
```

### Cleanup Old Data
```python
db.resume.cleanup_old(days=30)  # Remove old resume points
db.history.clear_recent()        # Clear recent files
```

---

## 🔄 Updating

To update to newer version:
1. Backup database: `cp /hdd/modernmedia_v5.db /tmp/backup.db`
2. Replace changed files only
3. Restart GUI
4. Check log for errors

Files that can be updated independently:
- `themes.py` - Add new themes
- `database/*.py` - Update operations
- `utils/*.py` - Update utilities
- `config.py` - Add settings

---

## 📝 Uninstallation

```bash
# Stop Enigma2
killall -9 enigma2

# Remove plugin
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/ModernMedia

# Optional: Remove data
rm /hdd/modernmedia_v5.db
rm -rf /hdd/.modernmedia_thumbs
rm -rf /tmp/modernmedia

# Restart
reboot
```

---

## ✅ Installation Checklist

- [ ] All 28 files copied
- [ ] Directory structure correct (database/, utils/, ui/)
- [ ] Permissions set (755)
- [ ] Enigma2 restarted
- [ ] Plugin appears in menu
- [ ] Database created
- [ ] Logs working
- [ ] Theme switching works
- [ ] Thumbnails generate
- [ ] No errors in log
- [ ] UI loads correctly
- [ ] Playback works
- [ ] Resume works

---

## 📞 Support

Check logs first:
```bash
tail -50 /tmp/modernmedia/plugin.log
```

Common issues documented in README_MODULAR.md

For development/debugging, see "Debugging Guide" in README_MODULAR.md
