import os
from .settings import *

# Production settings
DEBUG = True  # Temporary untuk debugging - set False setelah fix
ALLOWED_HOSTS = ['*']  # Temporary untuk debugging

# Environment variables untuk production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-)3m2xalpsagd^rl2x)tiznnfl4j&djvluddzc+^0#w@vxvs8vv')

# Allowed hosts untuk production - tambah domain khusus
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',     # Railway domain
    'web-production-7171.up.railway.app',  # Correct Railway URL
    'web-production-717f.up.railway.app',  # Previous URL (backup)
    '.vercel.app',      # Vercel domain
    '.herokuapp.com',   # Heroku domain
    '.render.com',      # Render domain
    '.fly.dev',         # Fly.io domain
    # Tambahkan domain khusus Anda di sini
    # 'yourdomain.com',
    # 'www.yourdomain.com',
]

# CORS settings untuk API (jika diperlukan)
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

# Tambahkan WhiteNoise middleware untuk static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Database untuk production - PostgreSQL prioritas utama
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Gunakan PostgreSQL dari environment (Railway, Heroku, dll)
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    # Fallback ke SQLite untuk development/testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files untuk production
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Hanya include jika direktori static ada
STATICFILES_DIRS = []
if (BASE_DIR / "static").exists():
    STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise settings untuk static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings untuk production publik
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings (aktifkan ketika sudah menggunakan domain dengan SSL)
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# CSRF settings - akan diaktifkan otomatis untuk HTTPS
CSRF_COOKIE_SECURE = False  # Set True ketika menggunakan HTTPS
SESSION_COOKIE_SECURE = False  # Set True ketika menggunakan HTTPS
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.vercel.app', 
    'https://*.herokuapp.com',
    'https://*.render.com',
    # Tambahkan domain Anda di sini
    # 'https://yourdomain.com',
]

# Cache untuk performa (menggunakan database)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

# Session settings untuk keamanan
SESSION_COOKIE_AGE = 3600  # 1 jam
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True

# Logging untuk production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}
