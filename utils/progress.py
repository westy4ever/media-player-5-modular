# ============================================================================
# ModernMedia/utils/progress.py v5.0 - Progress Bar Renderer
# ============================================================================

class ProgressBarRenderer:
    """
    Visual progress bar renderer
    Creates Unicode block-based progress bars
    """
    
    def __init__(self):
        self.empty = '░'
        self.filled = '█'
    
    def render(self, percentage, length=10):
        """
        Render progress bar
        
        Args:
            percentage: 0-100
            length: Number of blocks (default 10)
        
        Returns:
            String like "[████░░░░░░] 40%"
        """
        # Clamp percentage
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
        
        # Calculate filled blocks
        filled_count = int((percentage / 100.0) * length)
        empty_count = length - filled_count
        
        # Build bar
        bar = self.filled * filled_count + self.empty * empty_count
        
        return f"[{bar}] {int(percentage):3d}%"
    
    def render_mini(self, percentage):
        """Render compact 5-block bar"""
        return self.render(percentage, length=5)
    
    def render_compact(self, percentage):
        """Render very compact bar (no brackets/percentage)"""
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
        
        filled_count = int((percentage / 100.0) * 5)
        empty_count = 5 - filled_count
        
        return self.filled * filled_count + self.empty * empty_count
    
    def get_color(self, percentage):
        """
        Get suggested color for percentage
        
        Returns:
            Color name string
        """
        if percentage >= 95:
            return 'blue'    # Nearly complete
        elif percentage >= 70:
            return 'green'   # Most done
        elif percentage >= 30:
            return 'yellow'  # In progress
        else:
            return 'red'     # Just started
    
    def render_with_time(self, current_seconds, total_seconds):
        """Render progress bar with time information"""
        if total_seconds <= 0:
            return "[??????????] --:--"
        
        percentage = (current_seconds / total_seconds) * 100
        bar = self.render_compact(percentage)
        
        # Format time
        curr_mins = int(current_seconds // 60)
        curr_secs = int(current_seconds % 60)
        total_mins = int(total_seconds // 60)
        total_secs = int(total_seconds % 60)
        
        return f"[{bar}] {curr_mins}:{curr_secs:02d} / {total_mins}:{total_secs:02d}"
