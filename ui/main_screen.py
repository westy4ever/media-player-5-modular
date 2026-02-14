# ============================================================================
# ModernMedia/ui/main_screen.py v5.0 - Main Browser Screen
# ============================================================================

import os
import threading
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.Sources.StaticText import StaticText
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from enigma import eTimer, ePicLoad

from ..config import get_config
from ..constants import MEDIA_EXTENSIONS, ALTERNATIVE_PATHS, SORT_KEYS
from ..utils import SmartCache, ThumbnailManager, DirectoryScanner, ProgressBarRenderer
from ..utils.helpers import format_size, format_time, truncate_path, find_next_episode, find_subtitle
from .skins import SkinGenerator
from .menus import MenuHandler
from .player import ModernMediaPlayer

class ModernMediaScreen(Screen):
    """
    Main file browser screen
    Handles navigation, display, and user interactions
    """
    
    def __init__(self, session, db_instance):
        # Generate dynamic skin with current theme
        self.skin = SkinGenerator.generate_adaptive_skin()
        
        Screen.__init__(self, session)
        self.session = session
        self.db = db_instance
        
        # State
        self.current_path = self._get_start_dir()
        self.last_played_file = None
        self.scanner_thread = None
        self.search_query = ""
        
        # Components
        self.cache = SmartCache()
        self.thumb_mgr = ThumbnailManager()
        self.progress_renderer = ProgressBarRenderer()
        self.menu_handler = MenuHandler(self, db_instance)
        
        # Timers
        self.scan_timer = eTimer()
        self.scan_timer.callback.append(self._check_scan_status)
        # REMOVED: long_press_timer - not needed anymore
        
        # Poster loader
        self.poster_loader = ePicLoad()
        try:
            self.poster_loader.PictureData.get().append(self._poster_loaded_callback)
        except:
            pass
        
        # UI Widgets
        self._setup_widgets()
        
        # Actions
        self._setup_actions()
        
        # Initialize
        self.onLayoutFinish.append(self._startup)
    
    def _setup_widgets(self):
        """Setup UI widgets"""
        self["title"] = Label("Modern Media Player v5.0")
        self["counter"] = Label("")
        self["list"] = MenuList([])
        self["status"] = Label("Initializing...")
        self["info"] = Label("")
        self["poster"] = Pixmap()
        
        self["key_red"] = StaticText("Options")
        self["key_green"] = StaticText("Play")
        self["key_yellow"] = StaticText("Info")
        self["key_blue"] = StaticText("Menu")
    
    def _setup_actions(self):
        """Setup action mappings"""
        self["actions"] = ActionMap([
            "OkCancelActions", "ColorActions", "DirectionActions",
            "MenuActions", "NumberActions"
        ], {
            "ok": self._ok_pressed,
            "cancel": self._cancel_pressed,
            "green": self._green_pressed,
            "red": self._red_pressed,
            "yellow": self._yellow_pressed,
            "blue": self._blue_pressed,
            "menu": self._menu_pressed,
            "up": self._up_pressed,
            "down": self._down_pressed,
            "left": self["list"].pageUp,
            "right": self["list"].pageDown,
            "1": lambda: self.menu_handler.quick_action("favorites"),
            "2": lambda: self.menu_handler.quick_action("recent"),
            "3": lambda: self.menu_handler.quick_action("playlists"),
            "4": lambda: self.menu_handler.quick_action("search"),
            "5": lambda: self.menu_handler.quick_action("stats"),
            "6": self._cycle_view_mode,
            # REMOVED: Theme cycling (Key 7) - themes disabled
            "8": self._toggle_animations,
            "9": self._show_debug_info,
            "0": self._generate_thumbnails,
        }, -1)
    
    # === Initialization ===
    
    def _get_start_dir(self):
        """Get starting directory from config"""
        try:
            cfg = get_config()
            start = cfg.start_dir.value
            if os.path.exists(start):
                return start
        except:
            pass
        
        for path in ALTERNATIVE_PATHS:
            if os.path.exists(path):
                return path
        return "/media/"
    
    def _startup(self):
        """Called when screen is ready"""
        self._update_title()
        self["status"].setText("Ready")
        self.refresh_list()
    
    # === Display Updates ===
    
    def _update_title(self):
        """Update title bar with current path"""
        path = truncate_path(self.current_path)
        
        profile = ""
        try:
            cfg = get_config()
            if cfg.enable_profiles.value:
                profile = f" [{cfg.current_profile.value}]"
        except:
            pass
        
        self["title"].setText(f"Modern Media v5.0 - {path}{profile}")
    
    def refresh_list(self):
        """Refresh directory listing"""
        self._update_title()
        self._start_scan()
    
    # === Directory Scanning ===
    
    def _start_scan(self):
        """Start threaded directory scan"""
        if self.scanner_thread and self.scanner_thread.is_alive():
            self.scanner_thread.stop()
            self.scanner_thread.join(timeout=1.0)
        
        self.scanner_thread = DirectoryScanner(
            self.current_path, self.db, MEDIA_EXTENSIONS,
            self.search_query, self.cache
        )
        self.scanner_thread.start()
        self.scan_timer.start(200, True)
        
        self["status"].setText("⟳ Scanning...")
        self["list"].setList([("Scanning...", None, 'scan', None, None, 0)])
    
    def _check_scan_status(self):
        """Check if scan completed"""
        if self.scanner_thread and not self.scanner_thread.is_alive():
            self.scan_timer.stop()
            self._process_scan_results()
        else:
            self.scan_timer.start(200, True)
    
    def _process_scan_results(self):
        """Process and display scan results"""
        items = self.scanner_thread.results
        
        if self.scanner_thread.exception:
            self["status"].setText(f"Error: {str(self.scanner_thread.exception)[:40]}")
            return
        
        if not items:
            items = []
        
        # Search filter
        if self.search_query:
            items = [i for i in items if self.search_query.lower() in i[0].lower()]
        
        # Sort
        items = self._sort_items(items)
        
        # Add parent directory
        if self.current_path != "/":
            parent = os.path.dirname(self.current_path)
            items.insert(0, ("⬆ [UP] ..", parent, '..', None, None, 0))
        
        # Add progress bars
        items = self._add_progress_bars(items)
        
        # Check empty
        if not items or (len(items) == 1 and items[0][2] == '..'):
            items.append(("No media files", None, 'empty', None, None, 0))
        
        self["list"].setList(items)
        self._update_counter(items)
        self._update_status(items)
        self._update_poster()
    
    def _sort_items(self, items):
        """Sort items by configured key"""
        try:
            cfg = get_config()
            sort_key = cfg.sort_key.value
        except:
            sort_key = "name_asc"
        
        dirs = [i for i in items if i[2] == 'dir']
        files = [i for i in items if i[2] == 'file']
        
        if 'name' in sort_key:
            reverse = 'desc' in sort_key
            files.sort(key=lambda x: x[0].lower(), reverse=reverse)
        elif 'date' in sort_key:
            reverse = 'desc' in sort_key
            files.sort(key=lambda x: x[4] if x[4] else 0, reverse=reverse)
        elif 'size' in sort_key:
            reverse = 'desc' in sort_key
            files.sort(key=lambda x: x[3] if x[3] else 0, reverse=reverse)
        
        dirs.sort(key=lambda x: x[0].lower())
        return dirs + files
    
    def _add_progress_bars(self, items):
        """Add visual progress bars - RESTORED original working version"""
        try:
            cfg = get_config()
            if not cfg.show_progress_bars.value:
                return items
        except:
            return items
        
        enhanced = []
        for item in items:
            if item[2] == 'file' and item[5] > 0:
                resume_sec = item[5]
                size = item[3]
                
                # Estimate duration (1GB ≈ 1 hour for video)
                est_dur = int((size / (1024**3)) * 3600) if size else 0
                
                if est_dur > 0:
                    # Calculate percentage
                    pct = min((resume_sec / est_dur) * 100, 100)
                    
                    # Use the ProgressBarRenderer to create the bar
                    bar = self.progress_renderer.render_mini(pct)
                    
                    display = item[0]
                    # Remove old indicators
                    if " ▶ " in display:
                        display = display.split(" ▶ ")[0]
                    if " >> " in display:
                        display = display.split(" >> ")[0]
                    
                    # Add bar at the beginning (like original)
                    display = f"{bar} {display}"
                    enhanced.append((display, item[1], item[2], item[3], item[4], item[5]))
                else:
                    # No size info, just show time
                    mins = resume_sec // 60
                    secs = resume_sec % 60
                    display = item[0]
                    if " ▶ " in display:
                        display = display.split(" ▶ ")[0]
                    if " >> " in display:
                        display = display.split(" >> ")[0]
                    display = f"[{mins}:{secs:02d}] {display}"
                    enhanced.append((display, item[1], item[2], item[3], item[4], item[5]))
            else:
                enhanced.append(item)
        
        return enhanced
    
    def _update_counter(self, items):
        """Update file/directory counter"""
        files = len([i for i in items if i[2] == 'file'])
        dirs = len([i for i in items if i[2] == 'dir'])
        resume = len([i for i in items if i[2] == 'file' and i[5] > 0])
        
        self["counter"].setText(f"📁 {dirs} | 🎬 {files} | ▶ {resume}")
    
    def _update_status(self, items):
        """Update status bar"""
        files = len([i for i in items if i[2] == 'file'])
        dirs = len([i for i in items if i[2] == 'dir'])
        
        status = f"Ready - {files + dirs} items"
        if self.search_query:
            status += f" (search: {self.search_query})"
        
        self["status"].setText(status)
    
    # === Poster Display ===
    
    def _update_poster(self):
        """Update poster for selected item"""
        selected = self["list"].getCurrent()
        if not selected or selected[2] != 'file':
            self["info"].setText("")
            return
        
        file_path = selected[1]
        
        # Load thumbnail
        if self.thumb_mgr.has_thumb(file_path):
            thumb = self.thumb_mgr.get_thumb_path(file_path)
            self._load_poster_image(thumb)
        else:
            # Generate async
            def worker():
                thumb = self.thumb_mgr.generate(file_path)
                if thumb:
                    self._load_poster_image(thumb)
            threading.Thread(target=worker, daemon=True).start()
        
        # Update info
        self._update_info_panel(file_path, selected[3], selected[5])
    
    def _load_poster_image(self, image_path):
        """Load image into poster widget"""
        try:
            self.poster_loader.setPara((280, 420, 1, 1, False, 1, "#00000000"))
            self.poster_loader.startDecode(image_path)
        except:
            pass
    
    def _poster_loaded_callback(self, picInfo=None):
        """Callback when poster loaded"""
        try:
            ptr = self.poster_loader.getData()
            if ptr:
                self["poster"].instance.setPixmap(ptr)
        except:
            pass
    
    def _update_info_panel(self, file_path, size, resume_sec):
        """Update info sidebar"""
        lines = []
        
        if size:
            lines.append(format_size(size))
        
        if resume_sec > 0:
            lines.append(f"\nResume:\n{format_time(resume_sec)}")
        
        if self.db:
            try:
                if self.db.favorites.is_favorite(file_path):
                    lines.append("\n★ Favorite")
            except:
                pass
        
        self["info"].setText("\n".join(lines))
    
    # === Button Handlers ===
    
    def _ok_pressed(self):
        """OK button - play/enter - FIXED: No auto-menu"""
        # REMOVED: Long press timer that was auto-opening menu
        
        selected = self["list"].getCurrent()
        if not selected:
            return
        
        if selected[2] in ('..', 'dir'):
            self.current_path = selected[1]
            self.search_query = ""
            self.refresh_list()
        elif selected[2] == 'file':
            self._play_file(selected)
        
        self._update_poster()
    
    # REMOVED: _on_long_press method - no longer needed
    
    def _green_pressed(self):
        """Green - play selected"""
        selected = self["list"].getCurrent()
        if selected and selected[2] == 'file':
            self._play_file(selected)
    
    def _red_pressed(self):
        """Red - context menu"""
        selected = self["list"].getCurrent()
        if not selected:
            return
        
        if selected[2] == 'file':
            self.menu_handler.show_file_menu(selected)
        elif selected[2] == 'dir':
            self.menu_handler.show_dir_menu(selected)
    
    def _yellow_pressed(self):
        """Yellow - file info"""
        selected = self["list"].getCurrent()
        if selected and selected[2] == 'file':
            self.menu_handler.show_file_info(selected)
    
    def _blue_pressed(self):
        """Blue - quick menu"""
        self.menu_handler.show_quick_menu()
    
    def _menu_pressed(self):
        """Menu button"""
        self.menu_handler.show_quick_menu()
    
    def _up_pressed(self):
        """Up - move selection"""
        self["list"].up()
        self._update_poster()
    
    def _down_pressed(self):
        """Down - move selection"""
        self["list"].down()
        self._update_poster()
    
    def _cancel_pressed(self):
        """Cancel - go up or exit"""
        parent = os.path.dirname(self.current_path)
        
        try:
            at_start = self.current_path == self._get_start_dir()
        except:
            at_start = False
        
        if not at_start and self.current_path != "/" and parent:
            self.current_path = parent
            self.search_query = ""
            self.refresh_list()
        else:
            self.close()
    
    # === Keyboard Shortcuts ===
    
    def _cycle_view_mode(self):
        """Key 6 - cycle view modes"""
        modes = ["list", "details", "grid"]
        try:
            cfg = get_config()
            current = cfg.view_mode.value
            idx = modes.index(current)
            next_mode = modes[(idx + 1) % len(modes)]
            cfg.view_mode.value = next_mode
            cfg.view_mode.save()
            self._show_message(f"View: {next_mode}", "info", 2)
        except:
            pass
    
    # REMOVED: _cycle_theme method - themes disabled
    
    def _toggle_animations(self):
        """Key 8 - toggle animations"""
        try:
            cfg = get_config()
            current = cfg.show_animations.value
            cfg.show_animations.value = not current
            cfg.show_animations.save()
            self._show_message(f"Animations: {'ON' if not current else 'OFF'}", "info", 2)
        except:
            pass
    
    def _show_debug_info(self):
        """Key 9 - debug info"""
        import sys
        from ..constants import VERSION
        
        cache_stats = self.cache.get_stats()
        thumb_count = self.thumb_mgr.get_cache_count()
        
        info = (
            f"Debug Info\n\n"
            f"Version: {VERSION}\n"
            f"Python: {sys.version.split()[0]}\n"
            f"Path: {self.current_path}\n"
            f"DB: {'OK' if self.db else 'None'}\n"
            f"Cache: {cache_stats['total_entries']} entries\n"
            f"Thumbs: {thumb_count}"
        )
        self._show_message(info, "info", 8)
    
    def _generate_thumbnails(self):
        """Key 0 - batch generate thumbnails"""
        items = self["list"].list
        videos = [i[1] for i in items if i[2] == 'file']
        
        if not videos:
            self._show_message("No videos", "info", 2)
            return
        
        self["status"].setText(f"Generating {len(videos)} thumbnails...")
        
        def worker():
            for idx, video in enumerate(videos):
                self.thumb_mgr.generate(video)
                self["status"].setText(f"Generated {idx+1}/{len(videos)}")
            self["status"].setText("Thumbnails ready!")
        
        threading.Thread(target=worker, daemon=True).start()
    
    # === Playback ===
    
    def _play_file(self, item):
        """Play selected file"""
        file_path = item[1]
        size = item[3]
        mtime = item[4]
        
        if not os.path.exists(file_path):
            self._show_message("File not found", "error", 2)
            return
        
        # Check resume
        resume_sec = 0
        if self.db:
            try:
                resume_data = self.db.resume.get(file_path, size, mtime)
                resume_sec = resume_data.get('position_seconds', 0) if resume_data else 0
            except:
                pass
        
        # Ask resume or play
        if resume_sec > 0:
            try:
                cfg = get_config()
                action = cfg.default_resume_action.value
            except:
                action = "ask"
            
            if action == "resume":
                self._start_playback(file_path, resume_sec, size, mtime)
            elif action == "start":
                self._start_playback(file_path, 0, size, mtime)
            else:
                # FIXED: Yes = resume, No = start from beginning
                mins = resume_sec // 60
                secs = resume_sec % 60
                self.session.openWithCallback(
                    lambda choice: self._start_playback(file_path, resume_sec if choice else 0, size, mtime),
                    MessageBox,
                    f"Resume from {mins}:{secs:02d}?\n\n{os.path.basename(file_path)}\n\nYes = Resume | No = Start Over",
                    MessageBox.TYPE_YESNO,
                    timeout=10,
                    default=True
                )
        else:
            self._start_playback(file_path, 0, size, mtime)
    
    def _start_playback(self, file_path, start_pos, size, mtime):
        """Start video playback"""
        self.last_played_file = file_path
        
        # Add to recent
        if self.db:
            try:
                self.db.history.add_recent(file_path)
            except:
                pass
        
        # Find subtitle
        subtitle = find_subtitle(file_path)
        
        # Open player
        self.session.openWithCallback(
            self._playback_ended,
            ModernMediaPlayer,
            file_path, start_pos, self.db, size, mtime, subtitle
        )
    
    def _playback_ended(self):
        """Handle playback end - FIXED: Auto-play disabled by default"""
        if not self.last_played_file:
            self.refresh_list()
            return
        
        # Check if auto-play is enabled
        try:
            cfg = get_config()
            if not cfg.auto_play_next.value:
                # Auto-play disabled - just refresh
                self.refresh_list()
                return
        except:
            self.refresh_list()
            return
        
        # Auto-play is enabled - check for next episode
        next_file = find_next_episode(self.last_played_file, os.path.dirname(self.last_played_file))
        if next_file:
            self.session.openWithCallback(
                lambda choice: self._start_playback(next_file, 0, 0, 0) if choice else self.refresh_list(),
                MessageBox,
                f"Play next?\n\n{os.path.basename(next_file)}",
                MessageBox.TYPE_YESNO,
                timeout=10,
                default=True
            )
        else:
            self.refresh_list()
    
    # === Utilities ===
    
    def _show_message(self, msg, msg_type="info", timeout=3):
        """Show message box"""
        try:
            if msg_type == "error":
                mtype = MessageBox.TYPE_ERROR
            elif msg_type == "warning":
                mtype = MessageBox.TYPE_WARNING
            else:
                mtype = MessageBox.TYPE_INFO
            
            self.session.open(MessageBox, msg, mtype, timeout=timeout)
        except:
            self["status"].setText(msg[:50])
    
    # === Cleanup ===
    
    def close(self):
        """Clean up and close"""
        if self.scanner_thread:
            self.scanner_thread.stop()
            if self.scanner_thread.is_alive():
                self.scanner_thread.join(timeout=1.0)
        
        self.scan_timer.stop()
        # REMOVED: long_press_timer.stop() - timer no longer exists
        Screen.close(self)
