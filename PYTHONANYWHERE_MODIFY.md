# 🔧 MODIFY EXISTING PYTHONANYWHERE APP
# Jika ingin tetap pakai app yang ada

## Step 1: Add MPLS to Existing Project
```bash
# Masuk ke project directory yang sudah ada
cd /home/yourusername/existing_project

# Clone MPLS sebagai subdirectory
git clone https://github.com/trioagung/mpls_muhismart.git mpls

# Install dependencies MPLS
pip install Django==5.2.4 Pillow==11.3.0
```

## Step 2: Update URLs di Project Utama
Edit `existing_project/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('your_existing_app.urls')),  # App lama
    path('mpls/', include('mpls.mpls_muhismart.mpls.urls')),  # MPLS baru
]
```

## Step 3: Update Settings
Edit `existing_project/settings.py`:
```python
INSTALLED_APPS = [
    # ... existing apps
    'mpls.mpls_muhismart.main',
    'mpls.mpls_muhismart.panitia',
]

# Static files untuk MPLS
STATICFILES_DIRS = [
    BASE_DIR / 'mpls/mpls_muhismart/static',
]
```

## Step 4: Setup MPLS Database
```bash
# Setup MPLS database
cd mpls/mpls_muhismart
python manage.py makemigrations
python manage.py migrate

# Create superuser untuk MPLS
python manage.py createsuperuser
```

## Step 5: Access MPLS
- **Main app:** `https://yourusername.pythonanywhere.com/`
- **MPLS app:** `https://yourusername.pythonanywhere.com/mpls/`
- **MPLS admin:** `https://yourusername.pythonanywhere.com/mpls/admin/`

✅ **MPLS berjalan bersama app yang sudah ada!**
