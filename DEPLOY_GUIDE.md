# 🚀 PANDUAN DEPLOY KE PYTHONANYWHERE

## 📋 Langkah-langkah yang harus dilakukan di PythonAnywhere:

### 1. Login ke PythonAnywhere Console
- Buka https://www.pythonanywhere.com/
- Login ke akun trioagung64
- Buka "Consoles" > "Bash"

### 2. Fix Git Repository (Copy paste script ini di console):

```bash
cd /home/trioagung64
# Backup folder lama jika ada
if [ -d "mpls.muhismart" ]; then
    mv mpls.muhismart mpls.muhismart_backup_$(date +%Y%m%d_%H%M%S)
fi

# Clone repository terbaru
git clone https://github.com/trioagung/mpls_muhismart.git mpls.muhismart
cd mpls.muhismart

# Jalankan migrations
python3.11 manage.py migrate

# Restart web app
touch /var/www/trioagung64_pythonanywhere_com_wsgi.py
```

### 3. Verifikasi Deployment
- Buka website: https://trioagung64.pythonanywhere.com/
- Test menu "Koordinator Kelompok" - data sekarang akan tersimpan permanen
- Test user "anita" di menu "Jadwal Kegiatan" - permission sudah fixed

### 4. Jika masih ada masalah database:
```bash
cd /home/trioagung64/mpls.muhismart
python3.11 manage.py shell

# Di dalam shell Python:
from django.contrib.auth.models import User
from panitia.models import AksesMenu

# Cek user anita
user_anita = User.objects.filter(username='anita').first()
if user_anita:
    print("User anita ditemukan")
    akses = AksesMenu.objects.filter(user=user_anita, menu='Jadwal Kegiatan')
    print(f"Akses jadwal: {akses}")
else:
    print("User anita tidak ditemukan - perlu dibuat di admin")
```

## ✅ Setelah deployment berhasil:
- ✅ GitHub: **SUDAH DIPERBARUI**
- ✅ PythonAnywhere: **TINGGAL IKUTI LANGKAH DI ATAS**

## 🎯 Masalah yang telah diperbaiki:
1. **Koordinator Kelompok**: Data sekarang disimpan di database, tidak akan hilang lagi
2. **Permission System**: Sudah bekerja dengan benar, tinggal sync user di production
