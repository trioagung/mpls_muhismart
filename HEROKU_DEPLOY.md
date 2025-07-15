# 🚀 HEROKU DEPLOYMENT GUIDE
# MPLS MUHI SMART - Free Hosting Alternative

## Prerequisites
1. Create free Heroku account: https://heroku.com
2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

## Step 1: Prepare for Heroku
```bash
# Create Procfile
echo "web: gunicorn mpls.wsgi --log-file -" > Procfile

# Create runtime.txt
echo "python-3.10.14" > runtime.txt

# Update requirements.txt
pip freeze > requirements.txt
```

## Step 2: Update Settings for Heroku
Add to settings.py:
```python
import os
import dj_database_url

# Heroku settings
DEBUG = False
ALLOWED_HOSTS = ['*']

# Static files for Heroku
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database for Heroku
DATABASES['default'] = dj_database_url.config(default=f"sqlite:///{BASE_DIR}/db.sqlite3")
```

## Step 3: Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set config vars
heroku config:set DEBUG=False
heroku config:set SECRET_KEY='your-secret-key'

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## Step 4: Open Your App
```bash
heroku open
```

Your app will be at: https://your-app-name.herokuapp.com
