# 🔧 PYTHONANYWHERE WSGI CONFIGURATION
# Copy this content to your WSGI configuration file in PythonAnywhere

import os
import sys

# Add your project directory to the sys.path
path = '/home/YOURUSERNAME/mpls.muhismart'  # ⚠️ REPLACE 'YOURUSERNAME' with your actual username
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'mpls.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# 📝 INSTRUCTIONS:
# 1. Replace 'YOURUSERNAME' with your actual PythonAnywhere username
# 2. Copy this entire content to your WSGI configuration file
# 3. Save and reload your web app
# 4. Your Django app should be running!

# 🔍 TROUBLESHOOTING:
# - Check error logs if app doesn't load
# - Verify path exists: /home/YOURUSERNAME/mpls.muhismart
# - Ensure all requirements are installed
# - Check static/media files mapping in Web tab
