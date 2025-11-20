# config.py

from dataclasses import dataclass

@dataclass
class AppConfig:
    """Centralized application configuration"""
    PAGE_TITLE = "Resume Match Pro"
    PAGE_ICON = "📊"
    LAYOUT = "wide"
    
    # Score thresholds
    SCORE_EXCELLENT = 80
    SCORE_GOOD = 60
    SCORE_MODERATE = 40
    
    # UI Constants
    TEXTAREA_HEIGHT = 400
    
    # Colors
    COLOR_PRIMARY = "#667eea"
    COLOR_SECONDARY = "#764ba2"
    COLOR_SUCCESS = "#10b981"
    COLOR_WARNING = "#ef4444"