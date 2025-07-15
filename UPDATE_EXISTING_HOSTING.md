# 🔄 UPDATE HOSTING YANG SUDAH ADA
# Untuk mengembalikan ke hosting sebelumnya dengan code terbaru

## Jika Hosting di PythonAnywhere (Yang Sudah Ada):

### Step 1: Login ke Console PythonAnywhere
```bash
# Masuk ke directory project yang sudah ada
cd /home/yourusername/existing_project_directory

# Atau jika MPLS sudah ada disana:
cd /home/yourusername/mpls.muhismart
```

### Step 2: Update Code dari GitHub
```bash
# Pull updates terbaru
git pull origin main

# Atau jika ada conflict:
git reset --hard HEAD
git pull origin main
```

### Step 3: Install/Update Dependencies
```bash
# Install packages yang mungkin baru
pip install Django==5.2.4 Pillow==11.3.0 gunicorn whitenoise
```

### Step 4: Update Database
```bash
# Apply migrations terbaru
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Update Static Files
```bash
# Collect static files with updates
python manage.py collectstatic --noinput
```

### Step 6: Restart Web App
- Go to **PythonAnywhere Web tab**
- Click **"Reload"** button
- Your hosting will use the updated code!

## Jika Hosting di Platform Lain:

### For Railway/Render/Vercel:
```bash
# Just push to GitHub - auto deploy!
git add .
git commit -m "Update MPLS with latest fixes"
git push origin main
```

Platform akan otomatis deploy ulang dengan code terbaru.

✅ **Hosting kembali dengan semua fixes terbaru!**
