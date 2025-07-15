import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpls.settings')
django.setup()

from panitia.models import KoordinatorKelompok

# Tambah data test koordinator kelompok
test_data = [
    {"kelompok": "Kelompok A", "koordinator": "Ahmad\nSiti"},
    {"kelompok": "Kelompok B", "koordinator": "Budi\nAni"},
    {"kelompok": "Kelompok C", "koordinator": "Candra\nDewi"},
]

print("Menambah data test koordinator kelompok...")
for data in test_data:
    k, created = KoordinatorKelompok.objects.get_or_create(
        kelompok=data["kelompok"],
        defaults={"koordinator": data["koordinator"]}
    )
    if created:
        print(f"✅ Dibuat: {k.kelompok}")
    else:
        print(f"⚠️ Sudah ada: {k.kelompok}")

print(f"\nTotal koordinator kelompok: {KoordinatorKelompok.objects.count()}")

# Test format data yang akan dikirim ke template
print("\nData yang akan dikirim ke template:")
for k in KoordinatorKelompok.objects.all():
    print(f"- {k.kelompok}: {k.get_koordinator_list()}")
    
print("\n🎉 Data test siap! Refresh halaman struktur organisasi.")
