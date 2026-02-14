# ============================================================================
# ModernMedia/ui/menus.py v5.0 - Menu Handlers
# ============================================================================

import os
import time
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox
from Screens.VirtualKeyBoard import VirtualKeyBoard

from ..utils.helpers import format_size, format_time

class MenuHandler:
    """
    Handles all menu operations for ModernMediaScreen
    Separates menu logic from main screen logic
    """
    
    def __init__(self, screen, db):
        """
        Initialize menu handler
        
        Args:
            screen: ModernMediaScreen instance
            db: Database manager instance
        """
        self.screen = screen
        self.db = db
    
    # === Quick Actions ===
    
    def quick_action(self, action):
        """Handle quick action from number keys"""
        if action == "favorites":
            self.show_favorites()
        elif action == "recent":
            self.show_recent()
        elif action == "playlists":
            self.show_playlists()
        elif action == "search":
            self.open_search()
        elif action == "stats":
            self.show_stats()
    
    # === Main Menus ===
    
    def show_quick_menu(self):
        """Show quick menu (Blue button)"""
        menu = [
            ("🔄 Refresh", "refresh"),
            ("🔍 Search", "search"),
            ("⭐ Favorites", "favorites"),
            ("⏱️ Recent", "recent"),
            ("📋 Playlists", "playlists"),
            ("📊 Statistics", "stats"),
            ("📖 Bookmarks", "bookmarks"),
            ("⚙️ Settings", "settings"),
            ("❓ About", "about"),
        ]
        self.screen.session.openWithCallback(self._quick_menu_cb, ChoiceBox, title="Menu", list=menu)
    
    def _quick_menu_cb(self, result):
        """Quick menu callback"""
        if not result:
            return
        
        action = result[1]
        if action == "refresh":
            self.screen.cache.clear()
            self.screen.refresh_list()
        elif action == "search":
            self.open_search()
        elif action == "favorites":
            self.show_favorites()
        elif action == "recent":
            self.show_recent()
        elif action == "playlists":
            self.show_playlists()
        elif action == "stats":
            self.show_stats()
        elif action == "bookmarks":
            self.show_bookmarks()
        elif action == "settings":
            self.open_settings()
        elif action == "about":
            self.show_about()
    
    # === Context Menus ===
    
    def show_file_menu(self, item):
        """Show file context menu"""
        file_path = item[1]
        size = item[3]
        mtime = item[4]
        resume_sec = item[5]
        
        menu = [("▶ Play", "play")]
        
        if resume_sec > 0:
            menu.append((f"▶ Resume {format_time(resume_sec)}", "resume"))
            menu.append(("⟲ Start Over", "start"))
            menu.append(("✕ Clear Resume", "clear"))
        
        is_fav = False
        if self.db:
            try:
                is_fav = self.db.favorites.is_favorite(file_path)
            except:
                pass
        
        menu.append(("★ Remove Favorite" if is_fav else "☆ Add Favorite", "fav"))
        menu.append(("➕ Add to Playlist", "playlist"))
        menu.append(("ℹ File Info", "info"))
        menu.append(("🖼 Generate Thumbnail", "thumb"))
        
        self.screen.session.openWithCallback(
            lambda r: self._file_menu_cb(r, file_path, size, mtime, resume_sec),
            ChoiceBox,
            title=os.path.basename(file_path),
            list=menu
        )
    
    def _file_menu_cb(self, result, file_path, size, mtime, resume_sec):
        """File menu callback - SIMPLIFIED"""
        if not result:
            return
        
        action = result[1]
        
        if action == "play":
            # Play will handle resume logic automatically
            self.screen._play_file((file_path, None, 'file', size, mtime, resume_sec))
        elif action == "fav":
            if self.db:
                self.db.favorites.toggle(file_path)
                is_fav = self.db.favorites.is_favorite(file_path)
                self.screen._show_message("Added favorite ★" if is_fav else "Removed favorite", "info", 2)
                self.screen.refresh_list()
        elif action == "playlist":
            self._add_to_playlist_menu(file_path)
        elif action == "info":
            self.show_file_info((file_path, None, 'file', size, mtime, resume_sec))
        elif action == "thumb":
            import threading
            def worker():
                self.screen["status"].setText("Generating...")
                self.screen.thumb_mgr.generate(file_path)
                self.screen["status"].setText("Thumbnail ready!")
            threading.Thread(target=worker, daemon=True).start()
    
    def show_dir_menu(self, item):
        """Show directory context menu"""
        dir_path = item[1]
        
        menu = [
            ("📂 Open", "open"),
            ("📖 Bookmark", "bookmark"),
            ("🔄 Scan", "scan"),
            ("🖼 Generate Thumbs", "thumbs"),
        ]
        
        self.screen.session.openWithCallback(
            lambda r: self._dir_menu_cb(r, dir_path),
            ChoiceBox,
            title=os.path.basename(dir_path),
            list=menu
        )
    
    def _dir_menu_cb(self, result, dir_path):
        """Directory menu callback"""
        if not result:
            return
        
        if result[1] == "open":
            self.screen.current_path = dir_path
            self.screen.refresh_list()
        elif result[1] == "bookmark":
            self._add_bookmark(dir_path)
        elif result[1] == "scan":
            self.screen.cache.clear()
            self.screen.refresh_list()
        elif result[1] == "thumbs":
            self.screen.current_path = dir_path
            self.screen.refresh_list()
            self.screen._generate_thumbnails()
    
    # === Features ===
    
    def show_favorites(self):
        """Show favorites list"""
        if not self.db:
            return
        
        favs = self.db.favorites.get_all()
        if not favs:
            self.screen._show_message("No favorites\n\nPress RED to add!", "info", 3)
            return
        
        items = []
        for fav in favs:
            if os.path.exists(fav['file_path']):
                items.append((
                    f"★ {os.path.basename(fav['file_path'])}", 
                    fav['file_path'], 
                    'file', 
                    None, 
                    None, 
                    0
                ))
        
        self.screen["list"].setList(items)
        self.screen["status"].setText(f"Favorites - {len(items)} items")
        self.screen["counter"].setText("")
    
    def show_recent(self):
        """Show recent files"""
        if not self.db:
            return
        
        recent = self.db.history.get_recent(limit=30)
        if not recent:
            self.screen._show_message("No recent files", "info", 2)
            return
        
        items = []
        for rec in recent:
            if os.path.exists(rec['file_path']):
                played = time.strftime('%m/%d %H:%M', time.localtime(rec['played_date']))
                items.append((
                    f"{os.path.basename(rec['file_path'])} ({played})",
                    rec['file_path'], 
                    'file', 
                    None, 
                    None, 
                    0
                ))
        
        self.screen["list"].setList(items)
        self.screen["status"].setText(f"Recent - {len(items)}")
        self.screen["counter"].setText("")
    
    def show_playlists(self):
        """Show playlists"""
        if not self.db:
            return
        
        playlists = self.db.playlists.get_all()
        menu = [("+ Create New", "create")]
        for pl in playlists:
            menu.append((pl['name'], pl['playlist_id']))
        
        self.screen.session.openWithCallback(self._playlist_cb, ChoiceBox, title="Playlists", list=menu)
    
    def _playlist_cb(self, result):
        """Playlist menu callback"""
        if not result:
            return
        
        if result[1] == "create":
            self.screen.session.openWithCallback(
                self._create_playlist,
                VirtualKeyBoard,
                title="Playlist name:"
            )
        else:
            self._load_playlist(result[1])
    
    def _create_playlist(self, name):
        """Create new playlist"""
        if name and self.db:
            if self.db.playlists.create(name):
                self.screen._show_message(f"Created: {name}", "info", 2)
    
    def _load_playlist(self, playlist_id):
        """Load playlist items"""
        if not self.db:
            return
        
        items_data = self.db.playlists.get_items(playlist_id)
        items = []
        for item in items_data:
            if os.path.exists(item['file_path']):
                items.append((
                    os.path.basename(item['file_path']),
                    item['file_path'], 
                    'file', 
                    None, 
                    None, 
                    0
                ))
        
        self.screen["list"].setList(items)
        self.screen["status"].setText(f"Playlist - {len(items)}")
    
    def _add_to_playlist_menu(self, file_path):
        """Show add to playlist menu"""
        if not self.db:
            return
        
        playlists = self.db.playlists.get_all()
        menu = []
        for pl in playlists:
            menu.append((pl['name'], pl['playlist_id']))
        
        if not menu:
            self.screen._show_message("No playlists\n\nCreate one first!", "info", 2)
            return
        
        self.screen.session.openWithCallback(
            lambda r: self._add_to_playlist_cb(r, file_path),
            ChoiceBox,
            title="Add to playlist",
            list=menu
        )
    
    def _add_to_playlist_cb(self, result, file_path):
        """Add to playlist callback"""
        if result and self.db:
            if self.db.playlists.add_item(result[1], file_path):
                self.screen._show_message(f"Added to {result[0]}", "info", 2)
    
    def show_stats(self):
        """Show statistics"""
        if not self.db:
            return
        
        try:
            stats = self.db.statistics.get_stats(days=30)
            files = stats.get('total_files', 0)
            hours = stats.get('total_hours', 0)
            
            msg = (
                f"Statistics (30 Days)\n\n"
                f"Files: {files}\n"
                f"Time: {int(hours)}h {int((hours % 1) * 60)}m\n"
                f"Avg/Day: {files/30:.1f} files"
            )
            self.screen._show_message(msg, "info", 10)
        except:
            pass
    
    def show_bookmarks(self):
        """Show bookmarks"""
        if not self.db:
            return
        
        bookmarks = self.db.favorites.get_bookmarks()
        menu = []
        for bm in bookmarks:
            menu.append((bm['name'], bm['dir_path']))
        menu.append(("+ Add Current", "add"))
        
        self.screen.session.openWithCallback(self._bookmark_cb, ChoiceBox, title="Bookmarks", list=menu)
    
    def _bookmark_cb(self, result):
        """Bookmark callback"""
        if not result:
            return
        
        if result[1] == "add":
            self.screen.session.openWithCallback(
                lambda name: self._add_bookmark(self.screen.current_path, name),
                VirtualKeyBoard,
                title="Bookmark name:",
                text=os.path.basename(self.screen.current_path)
            )
        else:
            self.screen.current_path = result[1]
            self.screen.refresh_list()
    
    def _add_bookmark(self, path, name=None):
        """Add bookmark"""
        if not name:
            name = os.path.basename(path)
        
        if self.db and name:
            if self.db.favorites.add_bookmark(path, name):
                self.screen._show_message(f"Bookmark: {name}", "info", 2)
    
    def open_search(self):
        """Open search keyboard"""
        self.screen.session.openWithCallback(
            self._search_cb,
            VirtualKeyBoard,
            title="Search:",
            text=self.screen.search_query
        )
    
    def _search_cb(self, query):
        """Search callback"""
        self.screen.search_query = query if query else ""
        self.screen.refresh_list()
    
    def open_settings(self):
        """Open settings screen"""
        # Show current settings instead of "not implemented"
        try:
            cfg = get_config()
            
            settings_info = (
                "Current Settings\n\n"
                f"Start Dir: {cfg.start_dir.value}\n"
                f"Sort: {cfg.sort_key.value}\n"
                f"Resume: {cfg.default_resume_action.value}\n"
                f"Auto-play Next: {'ON' if cfg.auto_play_next.value else 'OFF'}\n"
                f"Progress Bars: {'ON' if cfg.show_progress_bars.value else 'OFF'}\n"
                f"Subtitles: {'Auto' if cfg.auto_load_subtitles.value else 'Manual'}\n\n"
                "To change settings:\n"
                "Edit /etc/enigma2/settings file"
            )
            self.screen._show_message(settings_info, "info", 10)
        except:
            self.screen._show_message("Settings\n\nUse config files to modify settings", "info", 3)
    
    def show_about(self):
        """Show about dialog"""
        from ..constants import VERSION
        
        about = (
            f"Modern Media Player v{VERSION}\n\n"
            "✨ Features:\n"
            "• Resume playback\n"
            "• Favorites & playlists\n"
            "• Watch history\n"
            "• Statistics tracking\n"
            "• Smart caching\n"
            "• 30+ improvements\n\n"
            "Shortcuts:\n"
            "0=Thumbs | 1=Favs | 2=Recent\n"
            "3=Playlist | 4=Search | 5=Stats\n"
            "6=View | 8=Anim | 9=Debug\n\n"
            "Modular Architecture v5.1"
        )
        self.screen._show_message(about, "info", 15)
    
    def show_file_info(self, item):
        """Show detailed file info"""
        file_path = item[0] if isinstance(item, tuple) else item
        size = item[3] if isinstance(item, tuple) and len(item) > 3 else None
        mtime = item[4] if isinstance(item, tuple) and len(item) > 4 else None
        
        try:
            if not size or not mtime:
                stats = os.stat(file_path)
                size = stats.st_size
                mtime = stats.st_mtime
            
            size_str = format_size(size)
            mod_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(mtime))
            
            resume_text = "No resume"
            if self.db:
                try:
                    resume_data = self.db.resume.get(file_path, size, mtime)
                    if resume_data:
                        resume_sec = resume_data.get('position_seconds', 0)
                        resume_text = f"Resume: {format_time(resume_sec)}"
                except:
                    pass
            
            info = (
                f"File Info\n\n"
                f"Name:\n{os.path.basename(file_path)}\n\n"
                f"Size: {size_str}\n"
                f"Modified: {mod_time}\n"
                f"{resume_text}"
            )
            self.screen._show_message(info, "info", 10)
        except:
            pass
