import zipfile
import os
from datetime import datetime

def create_upload_zip():
    """Buat file zip yang berisi file yang perlu diupload ke PythonAnywhere"""
    
    # Nama file zip dengan timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    zip_filename = f'mpls_upload_manual_{timestamp}.zip'
    
    # File content yang perlu dibuat/diupdate
    files_content = {
        'panitia/helpers.py': '''from .models import AksesMenu

def get_akses(user, menu):
    """
    Get user access with case-insensitive menu matching
    Fix untuk compatibility Windows → Linux hosting
    """
    if user.is_superuser:
        return True, True
    
    # Case-insensitive search untuk compatibility Windows → Linux
    akses_qs = AksesMenu.objects.filter(
        user=user, 
        menu__iexact=menu  # iexact = case-insensitive exact match
    )
    
    if akses_qs.exists():
        # Ambil entry mana saja yang bisa_edit True
        bisa_lihat = any(a.bisa_lihat for a in akses_qs)
        bisa_edit = any(a.bisa_edit for a in akses_qs)
        return bisa_lihat, bisa_edit
    return False, False
''',

        'panitia/views_koordinator_ajax.py': '''from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction, connection
from .models import KoordinatorKelompok
import json

@login_required
def tambah_koordinator_ajax(request):
    """AJAX endpoint untuk tambah koordinator kelompok"""
    if request.method == 'POST':
        try:
            kelompok = request.POST.get('kelompok', '').strip()
            koordinator_text = request.POST.get('koordinator', '').strip()
            
            print(f"[DEBUG] Received data - Kelompok: {kelompok}, Koordinator: {koordinator_text}")
            
            if not kelompok or not koordinator_text:
                return JsonResponse({
                    'success': False,
                    'error': 'Kelompok dan koordinator harus diisi!'
                })
            
            # Parse koordinator (satu per baris)
            koordinator_list = [k.strip() for k in koordinator_text.split('\\n') if k.strip()]
            
            if not koordinator_list:
                return JsonResponse({
                    'success': False,
                    'error': 'Minimal harus ada satu koordinator!'
                })
            
            print(f"[DEBUG] Parsed koordinator list: {koordinator_list}")
            
            # Cek duplikasi kelompok
            if KoordinatorKelompok.objects.filter(kelompok__iexact=kelompok).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'Kelompok "{kelompok}" sudah ada!'
                })
            
            # Simpan dengan atomic transaction
            with transaction.atomic():
                print(f"[DEBUG] Creating KoordinatorKelompok...")
                koordinator_obj = KoordinatorKelompok.objects.create(
                    kelompok=kelompok,
                    koordinator=koordinator_list
                )
                print(f"[DEBUG] Created object with ID: {koordinator_obj.id}")
                
                # Verify data tersimpan
                if KoordinatorKelompok.objects.filter(id=koordinator_obj.id).exists():
                    print(f"[DEBUG] Verification successful!")
                    return JsonResponse({
                        'success': True,
                        'message': f'Koordinator kelompok "{kelompok}" berhasil ditambahkan!',
                        'data': {
                            'kelompok': koordinator_obj.kelompok,
                            'koordinator': koordinator_obj.koordinator
                        }
                    })
                else:
                    print(f"[DEBUG] Verification failed!")
                    return JsonResponse({
                        'success': False,
                        'error': 'Data tidak tersimpan dengan benar!'
                    })
                    
        except Exception as e:
            print(f"[ERROR] Exception in tambah_koordinator_ajax: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Database error: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    })

@login_required
def test_database_connection(request):
    """Test database connection dan CRUD operations"""
    if request.method == 'POST':
        try:
            print("[DEBUG] Testing database connection...")
            
            # Test basic connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            print("[DEBUG] Basic connection OK")
            
            # Count existing koordinator
            koordinator_count = KoordinatorKelompok.objects.count()
            print(f"[DEBUG] Current koordinator count: {koordinator_count}")
            
            # Test create and delete
            test_obj = None
            try:
                test_obj = KoordinatorKelompok.objects.create(
                    kelompok='TEST_KELOMPOK_DELETE_ME',
                    koordinator=['Test User']
                )
                print(f"[DEBUG] Test create successful, ID: {test_obj.id}")
                test_create_delete = True
                test_obj.delete()
                print(f"[DEBUG] Test delete successful")
            except Exception as e:
                print(f"[DEBUG] Test create/delete failed: {str(e)}")
                test_create_delete = False
                if test_obj:
                    test_obj.delete()
            
            return JsonResponse({
                'success': True,
                'koordinator_count': koordinator_count,
                'test_create_delete': test_create_delete,
                'message': 'Database connection OK'
            })
            
        except Exception as e:
            print(f"[ERROR] Database test failed: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Database connection failed: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    })
''',

        'main/views.py': '''from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import os

def home(request):
    """Homepage dengan logo yang compatible untuk hosting"""
    # Use Django MEDIA_URL untuk compatibility dengan hosting environment
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
    
    if os.path.exists(logo_path):
        # Use MEDIA_URL yang sudah dikonfigurasi di settings
        logo_url = settings.MEDIA_URL + 'logo.png'
    else:
        logo_url = None
    
    context = {
        'logo_url': logo_url
    }
    return render(request, 'main/home.html', context)

@login_required
def upload_logo(request):
    """Upload logo sekolah"""
    if request.method == 'POST' and request.FILES.get('logo'):
        logo_file = request.FILES['logo']
        
        # Simpan ke media/logo.png
        logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
        
        # Pastikan direktori media ada
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # Simpan file
        with open(logo_path, 'wb+') as destination:
            for chunk in logo_file.chunks():
                destination.write(chunk)
        
        messages.success(request, 'Logo berhasil diupload!')
        return redirect('main:home')
    
    return render(request, 'main/upload_logo.html')
''',

        'DEPLOY_INSTRUCTIONS.md': '''# 🚀 INSTRUKSI DEPLOYMENT KE PYTHONANYWHERE

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
''',

        'README.md': '''# 📦 MPLS Upload Manual Package

File zip ini berisi perbaikan untuk aplikasi MPLS yang mengalami masalah di hosting PythonAnywhere.

## 🎯 Masalah yang Diperbaiki:

1. **Permission System** - User biasa tidak bisa edit menu jadwal
2. **Koordinator Kelompok** - Data tidak masuk di hosting
3. **Logo Border** - Logo PNG tampil dengan background kotak
4. **Case Sensitivity** - Windows → Linux compatibility

## 📁 Struktur File:

```
mpls_upload_manual_{timestamp}.zip
├── panitia/
│   ├── helpers.py                    # Case-insensitive permission
│   └── views_koordinator_ajax.py     # AJAX endpoints
├── main/
│   └── views.py                      # Logo URL fix
├── DEPLOY_INSTRUCTIONS.md            # Petunjuk deployment
└── README.md                         # File ini
```

## 🚀 Cara Deploy:

1. **Extract zip file** ini
2. **Backup data** di PythonAnywhere (penting!)
3. **Upload file** sesuai struktur direktori
4. **Run migration** jika diperlukan
5. **Restart web app**

## ✅ Expected Results:

Setelah deployment:
- ✅ Logo PNG tampil transparan tanpa border
- ✅ Koordinator kelompok bisa ditambah/edit di hosting
- ✅ Permission system working untuk user biasa
- ✅ Case sensitivity issue resolved

Ikuti instruksi di DEPLOY_INSTRUCTIONS.md untuk langkah detail!
'''
    }
    
    print(f"🔨 Membuat file zip: {zip_filename}")
    
    # Buat file zip
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Tambahkan file content yang sudah didefinisikan
        for file_path, content in files_content.items():
            zipf.writestr(file_path, content)
            print(f'✅ Added: {file_path}')
        
        # Tambahkan file existing jika ada
        existing_files = []
        
        # Cek dan tambahkan file yang sudah ada
        if os.path.exists('panitia/urls.py'):
            zipf.write('panitia/urls.py')
            existing_files.append('panitia/urls.py')
            print(f'✅ Added existing: panitia/urls.py')
    
    file_size = os.path.getsize(zip_filename)
    print(f'\n🎉 File zip berhasil dibuat!')
    print(f'📁 Nama file: {zip_filename}')
    print(f'📊 Ukuran: {file_size:,} bytes')
    print(f'📋 Total files: {len(files_content) + len(existing_files)}')
    
    print(f'\n📋 Langkah selanjutnya:')
    print(f'1. File zip tersimpan di: {os.path.abspath(zip_filename)}')
    print(f'2. Extract file zip')
    print(f'3. Upload file ke PythonAnywhere sesuai DEPLOY_INSTRUCTIONS.md')
    
    return zip_filename

if __name__ == '__main__':
    create_upload_zip()