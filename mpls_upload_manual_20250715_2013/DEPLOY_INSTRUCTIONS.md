# 🚀 INSTRUKSI DEPLOYMENT KE PYTHONANYWHERE

## 📋 File yang Diupload:

### 🔧 Backend Fixes:
- **panitia/helpers.py** - Case-insensitive permission system
- **panitia/views_koordinator_ajax.py** - AJAX endpoints untuk koordinator
- **main/views.py** - Logo URL fix untuk hosting

## 🔄 Langkah Upload Manual:

### 1. Backup Data (PENTING!)
```bash
cd /home/trioagung64
cp mpls.muhismart/db.sqlite3 backup_database_$(date +%Y%m%d_%H%M).sqlite3
cp -r mpls.muhismart/media backup_media_$(date +%Y%m%d_%H%M)
```

### 2. Upload Files via Files Tab PythonAnywhere:

Upload file-file berikut sesuai dengan path direktori:

1. **panitia/helpers.py** → `/home/trioagung64/mpls.muhismart/panitia/`
2. **panitia/views_koordinator_ajax.py** → `/home/trioagung64/mpls.muhismart/panitia/`
3. **main/views.py** → `/home/trioagung64/mpls.muhismart/main/`

### 3. Update URLs (jika belum ada):

Pastikan di `panitia/urls.py` ada endpoint AJAX:
```python
path('ajax/tambah-koordinator/', views_koordinator_ajax.tambah_koordinator_ajax, name='tambah_koordinator_ajax'),
path('ajax/test-database/', views_koordinator_ajax.test_database_connection, name='test_database'),
```

### 4. Run Migration:
```bash
cd /home/trioagung64/mpls.muhismart
python manage.py makemigrations
python manage.py migrate
python manage.py check
```

### 5. Restart Web App:
- Dashboard PythonAnywhere → Web tab → Reload button

### 6. Test Website:
1. ✅ Logo tampil tanpa border kotak
2. ✅ Login sebagai superuser
3. ✅ Test koordinator kelompok (tambah/edit)
4. ✅ Test permission system untuk user biasa

## 🎯 Fixes yang Diimplementasi:

- ✅ **Case-insensitive permission** untuk Windows→Linux compatibility
- ✅ **AJAX endpoints** untuk koordinator kelompok yang reliable
- ✅ **Enhanced error handling** dan debugging
- ✅ **Atomic transactions** untuk database reliability

## ⚠️ PENTING:
- Data user TIDAK akan hilang (database dan media files aman)
- Hanya file kode yang diupdate
- Backup sudah dilakukan sebelum upload
