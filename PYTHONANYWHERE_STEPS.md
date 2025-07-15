# 🚀 PYTHONANYWHERE DEPLOYMENT - SIMPLE STEPS
# Copy and paste these commands one by one in PythonAnywhere console

## Step 1: Fix Git Issues
```bash
cd ~/mpls.muhismart/mpls_muhismart
git reset --hard HEAD
git pull origin main
```

## Step 2: Install Dependencies
```bash
pip install Django==5.2.4 Pillow==11.3.0
```

## Step 3: Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 4: Create Superuser
```bash
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mplsmuhi.com', 'admin123')" | python manage.py shell
```

## Step 5: Setup Static Files
```bash
mkdir -p static media
python manage.py collectstatic --noinput
```

## Step 6: Create Logo
```bash
python -c "
from PIL import Image, ImageDraw
import os
img = Image.new('RGB', (200, 200), color='lightblue')
draw = ImageDraw.Draw(img)
draw.text((30, 80), 'SMA MUHI 1', fill='darkblue')
draw.text((50, 110), 'KARTASURA', fill='darkblue')
os.makedirs('media', exist_ok=True)
img.save('media/logo.png')
print('Logo created!')
"
```

## Step 7: Test Django
```bash
python manage.py check
```

## Step 8: Web App Configuration (PythonAnywhere Dashboard)
1. Go to **Web** tab
2. **Add new web app** → **Python 3.10** → **Manual**
3. **Source code:** `/home/YOURUSERNAME/mpls.muhismart/mpls_muhismart`
4. **WSGI file:** `/home/YOURUSERNAME/mpls.muhismart/mpls_muhismart/mpls/wsgi.py`

## Step 9: Static/Media Files Mapping
- **Static:** URL=`/static/` → Dir=`/home/YOURUSERNAME/mpls.muhismart/mpls_muhismart/static`
- **Media:** URL=`/media/` → Dir=`/home/YOURUSERNAME/mpls.muhismart/mpls_muhismart/media`

## Step 10: Reload & Test
- Click **Reload** button
- Visit: `https://YOURUSERNAME.pythonanywhere.com`
- Admin: `https://YOURUSERNAME.pythonanywhere.com/admin/`

## 🔐 Login Credentials
- **Username:** admin
- **Password:** admin123
