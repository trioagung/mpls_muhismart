# 🔄 UPDATE MPLS DI PYTHONANYWHERE YANG SUDAH ADA
# Untuk trioagung64.pythonanywhere.com

## Step 1: Login ke PythonAnywhere Console
Masuk ke: https://www.pythonanywhere.com/user/trioagung64/consoles/

## Step 2: Activate Virtual Environment
```bash
cd /home/trioagung64
source mpls-env/bin/activate
```

## Step 3: Navigate ke Project Directory
```bash
# Cari directory MPLS yang sudah ada
ls -la
# Kemungkinan ada di:
cd mpls.muhismart/mpls_muhismart
# ATAU
cd trioagung64  # sesuai screenshot
```

## Step 4: Update Code dari GitHub
```bash
# Pull latest updates dengan semua fixes
git pull origin main

# Jika ada conflict:
git reset --hard HEAD
git pull origin main
```

## Step 5: Install/Update Dependencies  
```bash
# Pastikan di virtual environment mpls-env
pip install Django==5.2.4 Pillow==11.3.0
```

## Step 6: Apply Database Updates
```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 7: Update Static Files
```bash
python manage.py collectstatic --noinput
```

## Step 8: Ensure Superuser Exists
```bash
# Create/update admin user
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mplsmuhi.com', 'admin123')" | python manage.py shell
```

## Step 9: Test Django
```bash
python manage.py check
```

## Step 10: Reload Web App
- Go to: https://www.pythonanywhere.com/user/trioagung64/webapps/
- Click **"Reload"** button for trioagung64.pythonanywhere.com

## ✅ RESULT:
**MPLS MUHI SMART updated di:** `https://trioagung64.pythonanywhere.com`

**Admin panel:** `https://trioagung64.pythonanywhere.com/admin/`

**Login:** 
- Username: admin
- Password: admin123

## 🔧 FIXES YANG AKAN ACTIVE:
- ✅ Logo tampil tanpa border yang tidak diinginkan
- ✅ Enhanced error handling 
- ✅ Case-insensitive permissions
- ✅ Improved media file handling
- ✅ All koordinator kelompok features working

**Perfect! Menggunakan hosting yang sudah ada adalah pilihan terbaik! 🚀**
