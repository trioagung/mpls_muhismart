# 📋 PANDUAN DETAIL PYTHONANYWHERE - STEP BY STEP
# Update MPLS MUHI SMART di trioagung64.pythonanywhere.com

## 🎯 OVERVIEW
Anda akan mengupdate MPLS yang sudah ada di PythonAnywhere dengan semua fixes terbaru (logo tanpa border, enhanced features, dll).

## 📝 YANG ANDA BUTUHKAN
- ✅ Akses ke akun PythonAnywhere: trioagung64
- ✅ Internet connection
- ✅ Browser (Chrome/Firefox/Edge)

## 🚀 LANGKAH 1: LOGIN KE PYTHONANYWHERE

### 1.1 Buka Browser
Buka browser favorit Anda

### 1.2 Login ke PythonAnywhere
- **URL:** https://www.pythonanywhere.com/login/
- **Username:** trioagung64
- **Password:** (password akun PythonAnywhere Anda)

### 1.3 Masuk ke Dashboard
Setelah login, Anda akan melihat dashboard PythonAnywhere

## 🖥️ LANGKAH 2: BUKA CONSOLE

### 2.1 Klik Menu "Consoles"
- Di dashboard, cari dan klik **"Consoles"**
- Atau langsung ke: https://www.pythonanywhere.com/user/trioagung64/consoles/

### 2.2 Buka Bash Console
- Klik **"Bash"** untuk membuka terminal baru
- Tunggu console loading (beberapa detik)

### 2.3 Console Siap
Anda akan melihat prompt seperti:
```
trioagung64@liveconsole123456:~$ 
```

## 📁 LANGKAH 3: NAVIGASI KE PROJECT

### 3.1 Cek Current Directory
Ketik command ini dan tekan Enter:
```bash
pwd
```
Output: `/home/trioagung64`

### 3.2 Lihat Isi Directory
```bash
ls -la
```
Anda akan melihat list file/folder. Cari folder project MPLS.

### 3.3 Masuk ke Virtual Environment
```bash
source mpls-env/bin/activate
```
Prompt akan berubah menjadi:
```
(mpls-env) trioagung64@liveconsole123456:~$
```

### 3.4 Cari Directory Project MPLS
```bash
# Cek apakah ada folder mpls.muhismart
ls -la | grep mpls

# Masuk ke directory project (pilih salah satu yang ada):
cd mpls.muhismart
# ATAU
cd mpls_muhismart  
# ATAU
cd trioagung64
```

### 3.5 Masuk ke Subfolder Django
```bash
# Lihat isi folder
ls -la

# Masuk ke subfolder yang berisi manage.py
# Biasanya ada 2 tingkat folder, contoh:
cd mpls_muhismart  # atau nama folder lain yang berisi manage.py
```

### 3.6 Verifikasi Location
```bash
# Pastikan ada file manage.py
ls manage.py
```
Output: `manage.py` (artinya lokasi sudah benar)

## 🔄 LANGKAH 4: UPDATE CODE DARI GITHUB

### 4.1 Reset Local Changes (Aman)
```bash
git reset --hard HEAD
```
Output: `HEAD is now at xxxxxx [commit message]`

### 4.2 Pull Updates Terbaru
```bash
git pull origin main
```
Anda akan melihat list file yang diupdate:
```
remote: Enumerating objects...
Updating xxxxxx..yyyyyy
Fast-forward
 main/views.py | xx insertions(+), xx deletions(-)
 main/templates/main/home.html | xx insertions(+), xx deletions(-)
 [... file lainnya]
```

## 📦 LANGKAH 5: UPDATE DEPENDENCIES

### 5.1 Install/Update Django & Pillow
```bash
pip install Django==5.2.4 Pillow==11.3.0
```
Output akan menampilkan:
```
Collecting Django==5.2.4
  Downloading Django-5.2.4-py3-none-any.whl
Installing collected packages: Django, Pillow
Successfully installed Django-5.2.4 Pillow-11.3.0
```

### 5.2 Verifikasi Installation
```bash
python -c "import django; print(django.get_version())"
```
Output: `5.2.4`

## 🗃️ LANGKAH 6: UPDATE DATABASE

### 6.1 Buat Migrations Baru (Jika Ada)
```bash
python manage.py makemigrations
```
Output bisa:
- `No changes detected` (normal)
- `Migrations for 'app_name': ...` (ada perubahan)

### 6.2 Apply Migrations
```bash
python manage.py migrate
```
Output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, main, panitia, sessions
Running migrations:
  No migrations to apply. (atau list migrations yang dijalankan)
```

## 📁 LANGKAH 7: UPDATE STATIC FILES

### 7.1 Collect Static Files
```bash
python manage.py collectstatic --noinput
```
Output:
```
Copying 'admin/css/base.css'
Copying 'admin/js/core.js'
...
xxx static files copied to '/home/trioagung64/path/to/static'.
```

## 👤 LANGKAH 8: SETUP ADMIN USER

### 8.1 Create/Update Admin User
Copy paste command ini (dalam 1 baris):
```bash
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mplsmuhi.com', 'admin123')" | python manage.py shell
```

Output:
- Jika user sudah ada: (no output)
- Jika user baru: `Superuser created successfully.`

## ✅ LANGKAH 9: TEST DJANGO

### 9.1 Check Django Configuration
```bash
python manage.py check
```
Output: `System check identified no issues (0 silenced).`

### 9.2 Test Database Connection
```bash
python manage.py shell -c "from django.contrib.auth.models import User; print(f'Users: {User.objects.count()}')"
```
Output: `Users: 1` (atau angka lain)

## 🌐 LANGKAH 10: RELOAD WEB APP

### 10.1 Buka Web App Dashboard
- Buka tab baru di browser
- URL: https://www.pythonanywhere.com/user/trioagung64/webapps/

### 10.2 Reload Application
- Cari web app dengan domain: `trioagung64.pythonanywhere.com`
- Klik tombol **"Reload"** (warna hijau)
- Tunggu sampai muncul "Reloaded successfully"

## 🎉 LANGKAH 11: TEST HASIL

### 11.1 Test Homepage
- Buka: https://trioagung64.pythonanywhere.com
- **CEK:** Logo tampil tanpa border yang tidak diinginkan
- **CEK:** Website loading normal

### 11.2 Test Admin Panel
- Buka: https://trioagung64.pythonanywhere.com/admin/
- **Login dengan:**
  - Username: `admin`
  - Password: `admin123`
- **CEK:** Admin panel accessible

### 11.3 Test Features
- **CEK:** Menu navigation works
- **CEK:** Panitia features functional
- **CEK:** Koordinator kelompok features working

## ✅ SELESAI!

**🎯 HASIL AKHIR:**
- ✅ MPLS MUHI SMART updated dengan semua fixes
- ✅ Logo display fixed (tanpa border yang tidak diinginkan)
- ✅ Enhanced error handling active
- ✅ All features working properly
- ✅ Live di: https://trioagung64.pythonanywhere.com

**🔐 LOGIN CREDENTIALS:**
- **URL:** https://trioagung64.pythonanywhere.com/admin/
- **Username:** admin
- **Password:** admin123

## 🆘 TROUBLESHOOTING

### Jika Ada Error:
1. **Check error logs** di PythonAnywhere dashboard
2. **Rerun commands** yang gagal
3. **Check console output** untuk detail error

### Jika Website Tidak Loading:
1. **Check Web App status** di dashboard
2. **Reload web app** sekali lagi
3. **Wait 1-2 menit** untuk propagation

### Jika Login Admin Gagal:
```bash
# Reset admin password
python manage.py changepassword admin
```

**🚀 MPLS MUHI SMART updated dan ready untuk production!**
