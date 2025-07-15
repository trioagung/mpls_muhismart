# 🚂 RAILWAY DEPLOYMENT GUIDE
# MPLS MUHI SMART - Modern Free Hosting

## Why Railway?
- ✅ Free tier dengan 500 hours/month
- ✅ Easy GitHub integration
- ✅ PostgreSQL database included
- ✅ Automatic deployments

## Step 1: Prepare Project
```bash
# Create railway.json
echo '{"version": 2}' > railway.json

# Create Procfile
echo "web: gunicorn mpls.wsgi --log-file -" > Procfile

# Update requirements.txt
echo "gunicorn==20.1.0" >> requirements.txt
echo "whitenoise==6.2.0" >> requirements.txt
```

## Step 2: Update Settings
Add to mpls/settings.py:
```python
import os

# Railway deployment settings
if 'RAILWAY_ENVIRONMENT' in os.environ:
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    
    # Static files
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## Step 3: Deploy to Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your mpls_muhismart repository
5. Railway will auto-deploy!

## Step 4: Setup Database
```bash
# Railway will provide PostgreSQL
# Add environment variables in Railway dashboard:
# DATABASE_URL (auto-provided)
# SECRET_KEY=your-secret-key
# DEBUG=False
```

## Step 5: Run Migrations
In Railway dashboard, go to deployments and run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

Your app will be at: https://your-app-name.railway.app
