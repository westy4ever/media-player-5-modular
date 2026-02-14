# ============================================================================
# ModernMedia/ui/player.py v5.0 - Video Player
# ============================================================================

import os
from Screens.InfoBar import MoviePlayer
from Components.ActionMap import ActionMap
from enigma import eTimer, eServiceReference

from ..config import get_config
from ..constants import MIN_RESUME_TIME, END_THRESHOLD

class ModernMediaPlayer(MoviePlayer):
    """
    Video player with resume functionality
    Handles playback, position saving, and end-of-file detection
    """
    
    def __init__(self, session, file_path, start_pos=0, db=None, 
                 file_size=0, mtime=0.0, subtitle_file=None):
        """
        Initialize player
        
        Args:
            session: Enigma2 session
            file_path: Path to video file
            start_pos: Start position in seconds
            db: Database manager instance
            file_size: File size for validation
            mtime: Modification time for validation
            subtitle_file: Optional subtitle file path
        """
        self.file_path = file_path
        self.start_pos = start_pos
        self.db = db
        self.file_size = file_size
        self.mtime = mtime
        self.subtitle_file = subtitle_file
        
        # Create service reference
        sref = eServiceReference(4097, 0, file_path)
        sref.setName(os.path.basename(file_path))
        
        # Initialize MoviePlayer
        MoviePlayer.__init__(self, session, sref)
        
        # Override actions
        self["MMActions"] = ActionMap(["OkCancelActions"], {
            "cancel": self.leavePlayer,
        }, 1)
        
        # Load subtitle if provided
        if subtitle_file:
            self._load_subtitle(subtitle_file)
        
        # Seek to start position
        if start_pos > 0:
            self.seek_timer = eTimer()
            self.seek_timer.callback.append(self._do_seek)
            self.seek_timer.start(2000, True)
        
        # Periodic save timer (every 30 seconds)
        self.save_timer = eTimer()
        self.save_timer.callback.append(self._periodic_save)
        self.save_timer.start(30000, False)
    
    def _load_subtitle(self, subtitle_path):
        """Load subtitle file"""
        try:
            if os.path.exists(subtitle_path):
                print(f"[Player] Subtitle: {subtitle_path}")
                # Enigma2 will auto-load if in same directory
        except:
            pass
    
    def _do_seek(self):
        """Seek to start position"""
        try:
            if self.start_pos <= 0:
                return
            
            start_pts = self.start_pos * 90000  # Convert to PTS
            seekable = self.getSeek()
            if seekable:
                result = seekable.seekTo(start_pts)
                if result == 0:
                    print(f"[Player] Seeked to {self.start_pos}s")
        except Exception as e:
            print(f"[Player] Seek error: {e}")
    
    def _periodic_save(self):
        """Periodically save position"""
        try:
            self._save_resume_position(periodic=True)
        except:
            pass
    
    def leavePlayer(self):
        """User pressed exit"""
        print("[Player] Leaving - saving position")
        self.save_timer.stop()
        self._save_resume_position()
        self.close()
    
    def leavePlayerOnExit(self):
        """Called on exit"""
        print("[Player] Exit event")
        self.save_timer.stop()
        self._save_resume_position()
        self.close()
    
    def doEofInternal(self, playing):
        """Called at end of file"""
        print("[Player] End of file")
        self.save_timer.stop()
        self._save_resume_position(is_eof=True)
        self.close()
    
    def _save_resume_position(self, is_eof=False, periodic=False):
        """
        Save current position to database
        
        Args:
            is_eof: True if at end of file
            periodic: True if periodic save
        """
        if not self.db or not self.file_path:
            return
        
        try:
            seekable = self.getSeek()
            if not seekable:
                return
            
            # Get current position
            position = seekable.getPlayPosition()
            if position[0] != 0:
                return
            
            position_sec = position[1] / 90000
            
            # Get total length
            length = seekable.getLength()
            if length[0] != 0:
                return
            
            length_sec = length[1] / 90000
            
            # Near end or at EOF - delete resume and mark watched
            if is_eof or position_sec >= (length_sec - END_THRESHOLD):
                print(f"[Player] Near end - deleting resume")
                self.db.resume.delete(self.file_path)
                
                # Add to watch history
                try:
                    cfg = get_config()
                    if cfg.enable_watch_history.value:
                        self.db.history.add_watch(self.file_path, int(position_sec))
                        
                        # Update statistics
                        duration_mins = int(position_sec // 60)
                        self.db.statistics.record_view(self.file_path, duration_mins)
                except:
                    pass
            
            # Save resume if significant time elapsed
            elif position_sec > MIN_RESUME_TIME:
                success = self.db.resume.set(
                    self.file_path,
                    int(position_sec),
                    self.file_size,
                    self.mtime
                )
                
                if success and not periodic:
                    mins = int(position_sec) // 60
                    secs = int(position_sec) % 60
                    print(f"[Player] Saved resume: {mins}:{secs:02d}")
        
        except Exception as e:
            print(f"[Player] Save error: {e}")
