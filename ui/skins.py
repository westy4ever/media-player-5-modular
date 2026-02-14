# ============================================================================
# ModernMedia/ui/skins.py v5.1 - Simple Skin (No Themes)
# ============================================================================

class SkinGenerator:
    """
    Simple skin generator - fixed dark theme only
    """
    
    @staticmethod
    def generate_main_screen_skin(theme_name=None):
        """
        Generate main browser screen skin - FIXED DARK THEME
        theme_name parameter ignored (kept for compatibility)
        """
        return """
<screen name="ModernMediaScreen" position="0,0" size="1920,1080" title="Modern Media v5.1" flags="wfNoBorder">
    <!-- Main background -->
    <panel position="0,0" size="1920,1080" backgroundColor="#DD000000" />
    
    <!-- Header bar -->
    <panel position="0,0" size="1920,120" backgroundColor="#EE1a1a1a" />
    <panel position="0,118" size="1920,2" backgroundColor="#FF00A8E6" />
    
    <!-- Title and counter -->
    <widget name="title" position="40,25" size="1200,70" font="Regular;42" foregroundColor="#FFFFFF" transparent="1" halign="left" valign="center"/>
    <widget name="counter" position="1260,35" size="620,50" font="Regular;32" foregroundColor="#00D4FF" transparent="1" halign="right" valign="center"/>
    
    <!-- Button bar -->
    <panel position="40,140" size="1840,100" backgroundColor="#AA1a1a1a" />
    <panel position="60,160" size="420,60" backgroundColor="#CC9f1313" />
    <panel position="500,160" size="420,60" backgroundColor="#CC1f771f" />
    <panel position="940,160" size="420,60" backgroundColor="#CCa08500" />
    <panel position="1380,160" size="420,60" backgroundColor="#CC18188b" />
    
    <widget source="key_red" render="Label" position="60,160" size="420,60" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="#ffffff" transparent="1" />
    <widget source="key_green" render="Label" position="500,160" size="420,60" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="#ffffff" transparent="1" />
    <widget source="key_yellow" render="Label" position="940,160" size="420,60" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="#ffffff" transparent="1" />
    <widget source="key_blue" render="Label" position="1380,160" size="420,60" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="#ffffff" transparent="1" />
    
    <!-- Main content area -->
    <panel position="40,260" size="1520,720" backgroundColor="#AA1a1a1a" />
    <widget name="list" position="60,280" size="1480,680" font="Regular;32" itemHeight="45" scrollbarMode="showOnDemand" foregroundColor="#E0E0E0" transparent="1" />
    
    <!-- Poster/info sidebar -->
    <panel position="1580,260" size="300,450" backgroundColor="#AA1a1a1a" />
    <widget name="poster" position="1590,270" size="280,420" alphatest="blend" />
    <widget name="info" position="1590,700" size="280,250" font="Regular;20" foregroundColor="#E0E0E0" transparent="1" halign="center" valign="top"/>
    
    <!-- Status bar -->
    <panel position="40,1000" size="1840,60" backgroundColor="#AA1a1a1a" />
    <widget name="status" position="60,1010" size="1800,40" font="Regular;28" foregroundColor="#00D4FF" transparent="1" halign="left" valign="center"/>
</screen>"""
    
    @staticmethod
    def generate_compact_skin(theme_name=None):
        """
        Generate compact 720p skin
        theme_name parameter ignored (kept for compatibility)
        """
        return """
<screen name="ModernMediaScreen" position="0,0" size="1280,720" title="Modern Media v5.1">
    <panel position="0,0" size="1280,720" backgroundColor="#DD000000" />
    <panel position="0,0" size="1280,80" backgroundColor="#EE1a1a1a" />
    
    <widget name="title" position="20,15" size="800,50" font="Regular;32" foregroundColor="#FFFFFF" transparent="1"/>
    <widget name="counter" position="840,20" size="420,40" font="Regular;24" foregroundColor="#00D4FF" transparent="1" halign="right"/>
    
    <panel position="20,100" size="1240,60" backgroundColor="#AA1a1a1a" />
    <widget source="key_red" render="Label" position="30,110" size="280,40" font="Regular;20" halign="center" valign="center" foregroundColor="#FFFFFF" transparent="1" />
    <widget source="key_green" render="Label" position="330,110" size="280,40" font="Regular;20" halign="center" valign="center" foregroundColor="#FFFFFF" transparent="1" />
    <widget source="key_yellow" render="Label" position="630,110" size="280,40" font="Regular;20" halign="center" valign="center" foregroundColor="#FFFFFF" transparent="1" />
    <widget source="key_blue" render="Label" position="930,110" size="280,40" font="Regular;20" halign="center" valign="center" foregroundColor="#FFFFFF" transparent="1" />
    
    <panel position="20,180" size="1020,480" backgroundColor="#AA1a1a1a" />
    <widget name="list" position="30,190" size="1000,460" font="Regular;24" itemHeight="35" foregroundColor="#E0E0E0" transparent="1" />
    
    <panel position="1060,180" size="200,300" backgroundColor="#AA1a1a1a" />
    <widget name="poster" position="1070,190" size="180,270" alphatest="blend" />
    <widget name="info" position="1070,470" size="180,190" font="Regular;16" foregroundColor="#E0E0E0" transparent="1"/>
    
    <panel position="20,680" size="1240,30" backgroundColor="#AA1a1a1a" />
    <widget name="status" position="30,685" size="1220,20" font="Regular;18" foregroundColor="#00D4FF" transparent="1"/>
</screen>"""
    
    @staticmethod
    def get_resolution():
        """Detect screen resolution"""
        try:
            from enigma import getDesktop
            desktop = getDesktop(0)
            size = desktop.size()
            return size.width(), size.height()
        except:
            return 1920, 1080
    
    @staticmethod
    def generate_adaptive_skin(theme_name=None):
        """
        Generate skin based on resolution
        theme_name parameter ignored (kept for compatibility)
        """
        width, height = SkinGenerator.get_resolution()
        
        if width <= 1280:
            return SkinGenerator.generate_compact_skin()
        else:
            return SkinGenerator.generate_main_screen_skin()
        
        return f"""
<screen name="ModernMediaScreen" position="0,0" size="1920,1080" title="Modern Media v5.0" flags="wfNoBorder">
    <!-- Main background -->
    <panel position="0,0" size="1920,1080" backgroundColor="{colors['bg_main']}" />
    
    <!-- Header bar -->
    <panel position="0,0" size="1920,120" backgroundColor="{colors['bg_header']}" />
    <panel position="0,118" size="1920,2" backgroundColor="{colors['accent']}" />
    
    <!-- Title and counter -->
    <widget name="title" position="40,25" size="1200,70" font="Regular;42" foregroundColor="{colors['text_primary']}" transparent="1" halign="left" valign="center"/>
    <widget name="counter" position="1260,35" size="620,50" font="Regular;32" foregroundColor="{colors['text_accent']}" transparent="1" halign="right" valign="center"/>
    
    <!-- Button bar -->
    <panel position="40,140" size="1840,100" backgroundColor="{colors['bg_panel']}" />
    <panel position="60,160" size="420,60" backgroundColor="{colors['btn_red']}" />
    <panel position="500,160" size="420,60" backgroundColor="{colors['btn_green']}" />
    <panel position="940,160" size="420,60" backgroundColor="{colors['btn_yellow']}" />
    <panel position="1380,160" size="420,60" backgroundColor="{colors['btn_blue']}" />
    
    <widget source="key_red" render="Label" position="60,160" size="420,60" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="#ffffff" transparent="1" />
    <widget source="key_green" render="Label" position="500,160" size="420,60" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="#ffffff" transparent="1" />
    <widget source="key_yellow" render="Label" position="940,160" size="420,60" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="#ffffff" transparent="1" />
    <widget source="key_blue" render="Label" position="1380,160" size="420,60" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="#ffffff" transparent="1" />
    
    <!-- Main content area -->
    <panel position="40,260" size="1520,720" backgroundColor="{colors['bg_panel']}" />
    <widget name="list" position="60,280" size="1480,680" font="Regular;32" itemHeight="45" scrollbarMode="showOnDemand" foregroundColor="{colors['text_secondary']}" transparent="1" />
    
    <!-- Poster/info sidebar -->
    <panel position="1580,260" size="300,450" backgroundColor="{colors['bg_panel']}" />
    <widget name="poster" position="1590,270" size="280,420" alphatest="blend" />
    <widget name="info" position="1590,700" size="280,250" font="Regular;20" foregroundColor="{colors['text_secondary']}" transparent="1" halign="center" valign="top"/>
    
    <!-- Status bar -->
    <panel position="40,1000" size="1840,60" backgroundColor="{colors['bg_panel']}" />
    <widget name="status" position="60,1010" size="1800,40" font="Regular;28" foregroundColor="{colors['text_accent']}" transparent="1" halign="left" valign="center"/>
</screen>"""
    
    @staticmethod
    def generate_compact_skin(theme_name=None):
        """Generate compact 720p skin"""
        colors = ThemeManager.get_theme_colors(theme_name)
        
        return f"""
<screen name="ModernMediaScreen" position="0,0" size="1280,720" title="Modern Media v5.0">
    <panel position="0,0" size="1280,720" backgroundColor="{colors['bg_main']}" />
    <panel position="0,0" size="1280,80" backgroundColor="{colors['bg_header']}" />
    
    <widget name="title" position="20,15" size="800,50" font="Regular;32" foregroundColor="{colors['text_primary']}" transparent="1"/>
    <widget name="counter" position="840,20" size="420,40" font="Regular;24" foregroundColor="{colors['text_accent']}" transparent="1" halign="right"/>
    
    <panel position="20,100" size="1240,60" backgroundColor="{colors['bg_panel']}" />
    <widget source="key_red" render="Label" position="30,110" size="280,40" font="Regular;20" halign="center" valign="center" foregroundColor="{colors['text_primary']}" transparent="1" />
    <widget source="key_green" render="Label" position="330,110" size="280,40" font="Regular;20" halign="center" valign="center" foregroundColor="{colors['text_primary']}" transparent="1" />
    <widget source="key_yellow" render="Label" position="630,110" size="280,40" font="Regular;20" halign="center" valign="center" foregroundColor="{colors['text_primary']}" transparent="1" />
    <widget source="key_blue" render="Label" position="930,110" size="280,40" font="Regular;20" halign="center" valign="center" foregroundColor="{colors['text_primary']}" transparent="1" />
    
    <panel position="20,180" size="1020,480" backgroundColor="{colors['bg_panel']}" />
    <widget name="list" position="30,190" size="1000,460" font="Regular;24" itemHeight="35" foregroundColor="{colors['text_secondary']}" transparent="1" />
    
    <panel position="1060,180" size="200,300" backgroundColor="{colors['bg_panel']}" />
    <widget name="poster" position="1070,190" size="180,270" alphatest="blend" />
    <widget name="info" position="1070,470" size="180,190" font="Regular;16" foregroundColor="{colors['text_secondary']}" transparent="1"/>
    
    <panel position="20,680" size="1240,30" backgroundColor="{colors['bg_panel']}" />
    <widget name="status" position="30,685" size="1220,20" font="Regular;18" foregroundColor="{colors['text_accent']}" transparent="1"/>
</screen>"""
    
    @staticmethod
    def get_resolution():
        """Detect screen resolution"""
        try:
            from enigma import getDesktop
            desktop = getDesktop(0)
            size = desktop.size()
            return size.width(), size.height()
        except:
            return 1920, 1080
    
    @staticmethod
    def generate_adaptive_skin(theme_name=None):
        """Generate skin based on resolution"""
        width, height = SkinGenerator.get_resolution()
        
        if width <= 1280:
            return SkinGenerator.generate_compact_skin(theme_name)
        else:
            return SkinGenerator.generate_main_screen_skin(theme_name)
