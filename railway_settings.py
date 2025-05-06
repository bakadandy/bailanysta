"""
This is a temporary settings bridge file to help Django find settings in Railway.
"""
import os
import sys
from pathlib import Path

# Add parent directory to Python path
APP_ROOT = Path(__file__).resolve().parent  # /app
BAILANYSTA_PROJECT_DIR = APP_ROOT / "bailanysta_project"  # /app/bailanysta_project
BAILANYSTA_PROJECT_SETTINGS_DIR = BAILANYSTA_PROJECT_DIR / "bailanysta_project"  # /app/bailanysta_project/bailanysta_project

# Add all possible import paths
sys.path.insert(0, str(APP_ROOT))  # /app
sys.path.insert(0, str(BAILANYSTA_PROJECT_DIR))  # /app/bailanysta_project
sys.path.insert(0, str(BAILANYSTA_PROJECT_SETTINGS_DIR))  # /app/bailanysta_project/bailanysta_project

# Import the actual settings module directly
from bailanysta_project.bailanysta_project.settings import *  # Import all settings 