# 🌐 UNIVERSAL HOSTING SETTINGS
# Add this to your mpls/settings.py for multiple hosting compatibility

import os
import dj_database_url

# Detect hosting environment
IS_HEROKU = 'DYNO' in os.environ
IS_RAILWAY = 'RAILWAY_ENVIRONMENT' in os.environ
IS_VERCEL = 'VERCEL_ENV' in os.environ
IS_RENDER = 'RENDER' in os.environ
IS_PYTHONANYWHERE = 'PYTHONANYWHERE_DOMAIN' in os.environ

# Production settings for any hosting
if any([IS_HEROKU, IS_RAILWAY, IS_VERCEL, IS_RENDER]):
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    
    # Static files configuration
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    # Add whitenoise for static files (except Vercel)
    if not IS_VERCEL:
        MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Database configuration
    if IS_VERCEL:
        # Vercel uses serverless, SQLite in /tmp
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': '/tmp/db.sqlite3',
            }
        }
    else:
        # Use DATABASE_URL if provided (Heroku, Railway, Render)
        default_db = f"sqlite:///{BASE_DIR}/db.sqlite3"
        DATABASES['default'] = dj_database_url.config(default=default_db)

# PythonAnywhere specific settings
elif IS_PYTHONANYWHERE:
    DEBUG = False  # Set to True for testing
    ALLOWED_HOSTS = ['*']
    
    # Keep existing SQLite database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Local development
else:
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
