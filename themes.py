# ============================================================================
# ModernMedia/themes.py v5.0 - Modular Theme System
# ============================================================================

from .config import get_config

class ThemeManager:
    """
    Theme management system
    Provides instant theme switching without restart
    """
    
    THEMES = {
        "dark": {
            "name": "Dark Theme",
            "description": "Default black background with blue accents",
            "colors": {
                "bg_main": "#DD000000",
                "bg_header": "#EE1a1a1a",
                "bg_panel": "#AA1a1a1a",
                "accent": "#FF00A8E6",
                "text_primary": "#FFFFFF",
                "text_secondary": "#E0E0E0",
                "text_accent": "#00D4FF",
                "btn_red": "#CC9f1313",
                "btn_green": "#CC1f771f",
                "btn_yellow": "#CCa08500",
                "btn_blue": "#CC18188b",
                "progress_bg": "#AA444444",
                "progress_fill": "#FF00A8E6",
            }
        },
        
        "light": {
            "name": "Light Theme",
            "description": "White background for daytime viewing",
            "colors": {
                "bg_main": "#DDFFFFFF",
                "bg_header": "#EEF5F5F5",
                "bg_panel": "#AAF0F0F0",
                "accent": "#FF0080D0",
                "text_primary": "#000000",
                "text_secondary": "#333333",
                "text_accent": "#0066CC",
                "btn_red": "#CCCC0000",
                "btn_green": "#CC009900",
                "btn_yellow": "#CCCC9900",
                "btn_blue": "#CC0000CC",
                "progress_bg": "#AACCCCCC",
                "progress_fill": "#FF0080D0",
            }
        },
        
        "blue": {
            "name": "Blue Theme",
            "description": "Ocean-inspired deep blue design",
            "colors": {
                "bg_main": "#DD001122",
                "bg_header": "#EE002244",
                "bg_panel": "#AA003366",
                "accent": "#FF00CCFF",
                "text_primary": "#FFFFFF",
                "text_secondary": "#DDDDFF",
                "text_accent": "#00DDFF",
                "btn_red": "#CC770000",
                "btn_green": "#CC007700",
                "btn_yellow": "#CC777700",
                "btn_blue": "#CC0033AA",
                "progress_bg": "#AA004488",
                "progress_fill": "#FF00CCFF",
            }
        },
        
        "netflix": {
            "name": "Netflix Style",
            "description": "Iconic red and black design",
            "colors": {
                "bg_main": "#DD000000",
                "bg_header": "#EE141414",
                "bg_panel": "#AA1a1a1a",
                "accent": "#FFE50914",
                "text_primary": "#FFFFFF",
                "text_secondary": "#B3B3B3",
                "text_accent": "#E50914",
                "btn_red": "#CCE50914",
                "btn_green": "#CC46D369",
                "btn_yellow": "#CCF5A623",
                "btn_blue": "#CC0071EB",
                "progress_bg": "#AA2a2a2a",
                "progress_fill": "#FFE50914",
            }
        },
        
        "plex": {
            "name": "Plex Style",
            "description": "Orange accents, modern media center look",
            "colors": {
                "bg_main": "#DD1a1a1a",
                "bg_header": "#EE282828",
                "bg_panel": "#AA333333",
                "accent": "#FFE5A00D",
                "text_primary": "#FFFFFF",
                "text_secondary": "#CCCCCC",
                "text_accent": "#E5A00D",
                "btn_red": "#CCCC0000",
                "btn_green": "#CC00AA00",
                "btn_yellow": "#CCE5A00D",
                "btn_blue": "#CC0066CC",
                "progress_bg": "#AA444444",
                "progress_fill": "#FFE5A00D",
            }
        }
    }
    
    @classmethod
    def get_current_theme(cls):
        """Get currently selected theme name"""
        try:
            cfg = get_config()
            return cfg.theme.value
        except:
            return "dark"
    
    @classmethod
    def get_theme_colors(cls, theme_name=None):
        """Get color scheme for a theme"""
        if theme_name is None:
            theme_name = cls.get_current_theme()
        
        theme = cls.THEMES.get(theme_name, cls.THEMES["dark"])
        return theme["colors"]
    
    @classmethod
    def get_theme_info(cls, theme_name):
        """Get theme metadata"""
        return cls.THEMES.get(theme_name, cls.THEMES["dark"])
    
    @classmethod
    def get_all_themes(cls):
        """Get list of all theme names"""
        return list(cls.THEMES.keys())
    
    @classmethod
    def get_theme_choices(cls):
        """Get theme choices for config"""
        return [(k, v["name"]) for k, v in cls.THEMES.items()]
    
    @classmethod
    def cycle_theme(cls):
        """Cycle to next theme"""
        themes = cls.get_all_themes()
        current = cls.get_current_theme()
        
        try:
            idx = themes.index(current)
            next_theme = themes[(idx + 1) % len(themes)]
            
            cfg = get_config()
            cfg.theme.value = next_theme
            cfg.theme.save()
            
            return next_theme
        except:
            return current
    
    @classmethod
    def validate_theme(cls, theme_name):
        """Check if theme exists"""
        return theme_name in cls.THEMES
