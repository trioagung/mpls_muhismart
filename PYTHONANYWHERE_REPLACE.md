# 🔄 REPLACE EXISTING PYTHONANYWHERE WEB APP
# Untuk akun gratis yang sudah punya web app

## Step 1: Backup Existing App (Opsional)
```bash
# Download existing code jika diperlukan
zip -r backup_old_app.zip /home/yourusername/old_project
```

## Step 2: Delete/Replace Old Project
```bash
# Hapus atau rename project lama
mv /home/yourusername/old_project /home/yourusername/old_project_backup

# Clone MPLS project
git clone https://github.com/trioagung/mpls_muhismart.git
cd mpls_muhismart/mpls_muhismart
```

## Step 3: Update Web App Configuration
Di **PythonAnywhere Web tab**:

1. **Source code:** `/home/yourusername/mpls_muhismart/mpls_muhismart`
2. **WSGI file:** `/home/yourusername/mpls_muhismart/mpls_muhismart/mpls/wsgi.py`

## Step 4: Update Static/Media Files
- **Static:** `/static/` → `/home/yourusername/mpls_muhismart/mpls_muhismart/static`
- **Media:** `/media/` → `/home/yourusername/mpls_muhismart/mpls_muhismart/media`

## Step 5: Setup MPLS
```bash
# Install dependencies
pip install Django==5.2.4 Pillow==11.3.0

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Step 6: Reload Web App
Click **"Reload"** button di Web tab

✅ **MPLS MUHI SMART akan menggantikan app lama!**
