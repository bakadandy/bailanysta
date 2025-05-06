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

# Calculate the path to the outer project directory (containing the apps)
# BASE_DIR = Path(__file__).resolve().parent.parent -> This points to bailanysta/bailanysta_project/bailanysta_project/
# We need the parent of that directory:
APPS_DIR = Path(__file__).resolve().parent.parent.parent # This should resolve to /app/bailanysta_project/

# Add the directory containing the apps ('users', 'posts', etc.) to sys.path
sys.path.insert(0, str(APPS_DIR))

# Set the settings module environment variable (already done via Railway Variables, but doesn't hurt)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bailanysta_project.bailanysta_project.settings')

application = get_wsgi_application()
