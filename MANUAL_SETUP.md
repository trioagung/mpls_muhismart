# 🔧 MANUAL PYTHONANYWHERE SETUP
# If automated scripts fail, follow these manual steps

## Step 1: Install Dependencies
```bash
pip install Django==5.2.4 Pillow==11.3.0
```

## Step 2: Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Create Superuser
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@mplsmuhi.com  
# Password: admin123
```

## Step 4: Collect Static Files
```bash
mkdir -p static
python manage.py collectstatic --noinput
```

## Step 5: Setup Media Directory
```bash
mkdir -p media
chmod 755 media
```

## Step 6: Create Logo Placeholder (Optional)
```python
# Run in Python shell
from PIL import Image, ImageDraw
import os

img = Image.new('RGB', (200, 200), color='lightblue')
draw = ImageDraw.Draw(img)
draw.text((50, 90), "SMA MUHI", fill='darkblue')
draw.text((60, 110), "LOGO", fill='darkblue')

os.makedirs('media', exist_ok=True)
img.save('media/logo.png')
```

## Step 7: Test Django
```bash
python manage.py check
python manage.py runserver
```

## Step 8: PythonAnywhere Web App Configuration
1. **Web tab** → **Add new web app**
2. **Python 3.10** → **Manual configuration**
3. **Source code:** `/home/YOURUSERNAME/mpls_muhismart/mpls_muhismart`
4. **WSGI file:** `/home/YOURUSERNAME/mpls_muhismart/mpls_muhismart/mpls/wsgi.py`

## Step 9: Static/Media Files
- **Static:** URL=`/static/` → Directory=`/home/YOURUSERNAME/mpls_muhismart/mpls_muhismart/static`
- **Media:** URL=`/media/` → Directory=`/home/YOURUSERNAME/mpls_muhismart/mpls_muhismart/media`

## Step 10: Reload & Test
- Click **"Reload"** button
- Visit: `https://YOURUSERNAME.pythonanywhere.com`
- Test admin: `https://YOURUSERNAME.pythonanywhere.com/admin/`
