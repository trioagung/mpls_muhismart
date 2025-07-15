# ⚡ VERCEL DEPLOYMENT GUIDE
# MPLS MUHI SMART - Serverless Hosting

## Why Vercel?
- ✅ Unlimited bandwidth
- ✅ GitHub integration
- ✅ Global CDN
- ✅ Easy setup

## Step 1: Create Vercel Config
```json
{
  "version": 2,
  "builds": [
    {
      "src": "mpls/wsgi.py",
      "use": "@vercel/python",
      "config": { "maxLambdaSize": "15mb", "runtime": "python3.9" }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "mpls/wsgi.py"
    }
  ]
}
```

## Step 2: Update Settings
Add to mpls/settings.py:
```python
import os

# Vercel deployment
if 'VERCEL_ENV' in os.environ:
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    
    # Database - use SQLite for simplicity
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',
        }
    }
```

## Step 3: Deploy to Vercel
1. Go to https://vercel.com
2. Sign up with GitHub
3. Import your repository
4. Vercel will auto-deploy!

## Step 4: Environment Variables
In Vercel dashboard, add:
- SECRET_KEY=your-secret-key
- DEBUG=False

Your app will be at: https://your-app-name.vercel.app
