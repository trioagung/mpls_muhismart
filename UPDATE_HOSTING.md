# Update Hosting PythonAnywhere

## Panduan Update Hosting yang Sudah Ada (trioagung64.pythonanywhere.com)

### Langkah-langkah Update:

1. **Login ke PythonAnywhere Dashboard**
   - Buka: https://www.pythonanywhere.com/
   - Login dengan akun trioagung64

2. **Update Code dari GitHub**
   ```bash
   # Masuk ke console bash di PythonAnywhere
   cd /home/trioagung64/mpls_muhismart
   git pull origin main
   ```

3. **Update Requirements (jika ada perubahan)**
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

4. **Jalankan Migrasi Database**
   ```bash
   python3.10 manage.py makemigrations
   python3.10 manage.py migrate
   ```

5. **Collect Static Files**
   ```bash
   python3.10 manage.py collectstatic --noinput
   ```

6. **Reload Web App**
   - Buka tab "Web" di dashboard PythonAnywhere
   - Klik tombol "Reload trioagung64.pythonanywhere.com"

### Catatan Penting:
- **JANGAN** hapus database yang sudah ada (db.sqlite3) karena sudah berisi data publik
- **PASTIKAN** backup data sebelum update besar
- Domain public: trioagung64.pythonanywhere.com sudah berjalan dengan data

### Files yang Diperbaiki:
- ✅ Logo tampil dengan baik (tanpa border)
- ✅ Profile foto tampil persegi panjang untuk PNG
- ✅ Sistem permission case-insensitive (Windows ↔ Linux)
- ✅ Media files handling diperbaiki
- ✅ **JADWAL KELOMPOK:** Sekarang tersimpan permanen di database (tidak hilang saat logout/login)
- ✅ **MULTI-USER SYNC:** Semua user melihat jadwal yang sama secara real-time

### Update Terbaru (16 Juli 2025):
**JADWAL KELOMPOK FIXED!** 
- Data jadwal sekarang tersimpan di database, bukan session
- Tidak akan hilang saat logout/login
- Semua user melihat perubahan secara langsung
- Data permanen dan aman

Proyek sudah dibersihkan dan siap untuk update hosting yang sudah ada.
