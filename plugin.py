# ============================================================================
# ModernMedia/plugin.py v5.0 - Modular Entry Point
# ============================================================================

import sys
import os
import time
import traceback
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox

from .utils.helpers import setup_logging, log_message, detect_environment
from .config import init_config
from .constants import VERSION

def main(session, **kwargs):
    """Main plugin entry point"""
    log_message("="*60)
    log_message(f"Modern Media Player v{VERSION} Starting")
    log_message("ALL IMPROVEMENTS ACTIVE - MODULAR ARCHITECTURE")
    
    # Log environment
    env = detect_environment()
    log_message(f"Python: {env['python_version']}")
    log_message(f"Image: {env['image']}")
    log_message(f"Platform: {env['platform']}")
    
    try:
        # Import UI components
        log_message("Loading UI components...")
        from .ui.main_screen import ModernMediaScreen
        log_message("UI components loaded ✓")
        
        # Import database
        log_message("Initializing database...")
        from .database.connection import DatabaseManager
        db = DatabaseManager()
        log_message(f"Database ready ✓ ({db.get_size_mb():.2f} MB)")
        
        # Initialize config
        log_message("Loading configuration...")
        if init_config():
            log_message("Configuration loaded ✓")
        
        # Open main screen
        log_message("Opening main screen...")
        result = session.open(ModernMediaScreen, db)
        log_message("Application started successfully ✓")
        log_message("="*60)
        return result
        
    except Exception as e:
        error_details = traceback.format_exc()
        log_message("FATAL ERROR:")
        log_message(error_details)
        log_message("="*60)
        
        error_msg = (
            f"Modern Media Player Error\n\n"
            f"{str(e)[:150]}\n\n"
            f"Check log: /tmp/modernmedia/plugin.log"
        )
        
        return session.open(MessageBox, error_msg, MessageBox.TYPE_ERROR, timeout=10)

def Plugins(**kwargs):
    """Plugin descriptor"""
    log_message(f"Registering Modern Media Player v{VERSION}")
    
    return PluginDescriptor(
        name=f"Modern Media Player v{VERSION}",
        description="Modular architecture - All 36+ features - Professional grade",
        where=PluginDescriptor.WHERE_PLUGINMENU,
        fnc=main,
        needsRestart=False
    )
