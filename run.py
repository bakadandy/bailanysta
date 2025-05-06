#!/usr/bin/env python
"""
Startup script for Railway deployment that handles path setup
and launches gunicorn with the correct settings.
"""
import os
import sys
import subprocess
from pathlib import Path

# Add all relevant directories to Python's import path
BASE_DIR = Path(__file__).resolve().parent  # /app
sys.path.insert(0, str(BASE_DIR))  # /app
sys.path.insert(0, str(BASE_DIR / "bailanysta_project"))  # /app/bailanysta_project
sys.path.insert(0, str(BASE_DIR / "bailanysta_project" / "bailanysta_project"))  # /app/bailanysta_project/bailanysta_project

# Set the correct settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bailanysta_project.bailanysta_project.settings")

# Run migrations first (comment this out if migrations run successfully)
try:
    print("Running migrations...")
    subprocess.run(
        ["python", "bailanysta_project/manage.py", "migrate", "--noinput"], 
        check=True
    )
    print("Migrations complete!")
except subprocess.CalledProcessError as e:
    print(f"Error running migrations: {e}")
    # Continue anyway - we'll still try to start the server

# Launch Gunicorn
print("Starting Gunicorn...")
os.execvp("gunicorn", [
    "gunicorn",
    "bailanysta_project.bailanysta_project.wsgi",
    "--log-file", "-",
    "--bind", "0.0.0.0:8080"
]) 