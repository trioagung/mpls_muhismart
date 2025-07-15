# 📦 MPLS Upload Manual Package

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
