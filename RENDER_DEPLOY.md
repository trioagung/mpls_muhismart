# 🎨 RENDER DEPLOYMENT GUIDE
# MPLS MUHI SMART - Reliable Free Hosting

## Why Render?
- ✅ 750 hours/month free
- ✅ PostgreSQL database included
- ✅ Easy GitHub deployment
- ✅ Automatic SSL

## Step 1: Prepare for Render
```bash
# Create build script
cat > build.sh << 'EOF'
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
EOF

chmod +x build.sh

# Update requirements.txt
echo "gunicorn==20.1.0" >> requirements.txt
echo "psycopg2-binary==2.9.5" >> requirements.txt
```

## Step 2: Update Settings for Render
Add to mpls/settings.py:
```python
import os
import dj_database_url

# Render deployment
if 'RENDER' in os.environ:
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    
    # Database
    DATABASES['default'] = dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
    
    # Static files
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## Step 3: Deploy to Render
1. Go to https://render.com
2. Sign up with GitHub
3. Create "New Web Service"
4. Connect your repository
5. Configure:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn mpls.wsgi:application`
   - Environment: Python 3

## Step 4: Environment Variables
Add in Render dashboard:
- SECRET_KEY=your-secret-key
- DEBUG=False
- DATABASE_URL (auto-provided)

## Step 5: Create Superuser
In Render shell, run:
```bash
python manage.py createsuperuser
```

Your app will be at: https://your-app-name.onrender.com
