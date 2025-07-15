import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpls.settings')
django.setup()

from panitia.models import PanitiaUtama

print(f"Total Panitia Utama di database: {PanitiaUtama.objects.count()}")
print("\nData yang ada:")
for i, p in enumerate(PanitiaUtama.objects.all(), 1):
    print(f"{i}. {p.jabatan} (kedudukan: {p.kedudukan})")
    print(f"   Anggota: {p.anggota[:100]}...")
    print()

if PanitiaUtama.objects.count() == 0:
    print("❌ Tidak ada data di database!")
    print("Kemungkinan masalah:")
    print("1. Form tidak mengirim data dengan benar")
    print("2. Ada error saat save ke database")
    print("3. Permission tidak diizinkan")
else:
    print("✅ Data ditemukan di database")
