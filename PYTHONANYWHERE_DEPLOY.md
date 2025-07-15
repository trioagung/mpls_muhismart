# 🚀 AUTOMATED DEPLOYMENT - PYTHONANYWHERE INSTRUCTIONS

## 📝 **LANGKAH OTOMATIS - IKUTI URUTAN INI:**

### **1️⃣ SETUP REPOSITORY DI PYTHONANYWHERE**

Buka **Console** di PythonAnywhere dan jalankan:

```bash
# Clone repository dari GitHub
git clone https://github.com/[USERNAME]/mpls.muhismart.git
cd mpls.muhismart

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install django

# Run automated deployment script
chmod +x deploy.sh
./deploy.sh
```

### **2️⃣ SETUP WEB APP DI PYTHONANYWHERE**

1. **Buka Web tab** di PythonAnywhere Dashboard
2. **Create New Web App** → Python 3.10 → Manual Configuration
3. **Set Source Code**: `/home/[username]/mpls.muhismart`
4. **Set Working Directory**: `/home/[username]/mpls.muhismart`

### **3️⃣ KONFIGURASI WSGI FILE**

Edit WSGI file di: `/home/[username]/mpls.muhismart/mpls/wsgi.py`

Ganti isinya dengan:
```python
import os
import sys

# Add project directory to path
path = '/home/[username]/mpls.muhismart'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpls.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### **4️⃣ SETUP STATIC DAN MEDIA FILES**

Di **Web tab**, tambahkan **Static files mappings**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/[username]/mpls.muhismart/static` |
| `/media/` | `/home/[username]/mpls.muhismart/media` |

### **5️⃣ FINAL SETUP**

Kembali ke Console:
```bash
cd mpls.muhismart
source .venv/bin/activate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
# Username: admin
# Password: [pilih password yang aman]
```

### **6️⃣ RELOAD WEB APP**

- Klik **"Reload [domain].pythonanywhere.com"** di Web tab
- Tunggu hingga status menunjukkan **"Running"**

## 🎯 **TESTING**

### **✅ Test Checklist:**

1. **Homepage**: `https://[domain].pythonanywhere.com/`
   - ✅ Logo tampil tanpa border (persegi panjang)
   - ✅ Menu navigation bekerja
   
2. **Admin Panel**: `https://[domain].pythonanywhere.com/admin/`
   - ✅ Login dengan kredensial yang dibuat
   - ✅ Styling Django admin tampil normal
   
3. **Panitia Features**: 
   - ✅ Struktur organisasi accessible
   - ✅ Koordinator kelompok bisa diinput dan tersimpan
   - ✅ Data persisten antar reload

4. **Media Files**:
   - ✅ Upload logo bekerja
   - ✅ Logo tampil di homepage

## 🆘 **TROUBLESHOOTING**

### **Jika Logo Tidak Tampil:**
```bash
# Check media directory permissions
ls -la media/
chmod 755 media/
chmod 644 media/logo.png
```

### **Jika Django Admin Tidak Styled:**
```bash
# Rerun collectstatic
python manage.py collectstatic --noinput --clear
```

### **Jika Data Tidak Tersimpan:**
```bash
# Check database permissions
ls -la db.sqlite3
chmod 644 db.sqlite3
```

## 📞 **SUPPORT**

Jika ada masalah, check:
1. **Error logs** di PythonAnywhere Console: `tail -f /var/log/[username].pythonanywhere.com.error.log`
2. **Django logs**: `tail -f django.log`

## 🎉 **SELESAI!**

Aplikasi MPLS MUHI SMART sekarang sudah:
- ✅ **Deployed otomatis** ke PythonAnywhere
- ✅ **Logo tampil** tanpa border yang tidak diinginkan
- ✅ **All features working** dalam production environment
- ✅ **Static files** properly served
- ✅ **Media uploads** functional
- ✅ **Database** persistent dan working

**URL Aplikasi**: `https://[domain].pythonanywhere.com/`
**Admin Panel**: `https://[domain].pythonanywhere.com/admin/`

🚀 **Happy coding!**
