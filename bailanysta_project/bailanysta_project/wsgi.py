"""
WSGI config for bailanysta_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Calculate the path to the directory containing the app folders ('users', 'posts', etc.)
# This should resolve to /app/bailanysta_project/
APPS_DIR = Path(__file__).resolve().parent.parent

# Add the apps directory to the start of Python's import path
sys.path.insert(0, str(APPS_DIR))

# Set the settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bailanysta_project.bailanysta_project.settings')

application = get_wsgi_application()
