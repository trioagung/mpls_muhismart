import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpls.settings')
django.setup()

from panitia.models import PanitiaUtama, KoordinatorKelompok

print("=== STATUS DATABASE ===")
print(f"PanitiaUtama count: {PanitiaUtama.objects.count()}")
print(f"KoordinatorKelompok count: {KoordinatorKelompok.objects.count()}")

print("\n=== DATA PANITIA UTAMA ===")
for p in PanitiaUtama.objects.all():
    print(f"- {p.jabatan} (kedudukan: {p.kedudukan})")
    print(f"  Anggota: {p.anggota[:50]}...")

print("\n=== DATA KOORDINATOR KELOMPOK ===")
for k in KoordinatorKelompok.objects.all():
    print(f"- {k.kelompok}")
    print(f"  Koordinator: {k.get_koordinator_list()}")

print("\n=== TEST VIEW CONTEXT ===")
from collections import defaultdict

# Simulasi data yang akan dikirim ke template
struktur_sorted = list(PanitiaUtama.objects.all().order_by('kedudukan', 'jabatan'))
piramida = defaultdict(list)

for item in struktur_sorted:
    piramida[item.kedudukan].append({
        'nama': item.jabatan,
        'kedudukan': item.kedudukan,
        'anggota': item.anggota_list(),
        'tugas': '',
    })

koordinator_list = KoordinatorKelompok.objects.all().order_by('kelompok')
koordinator_data = []
for k in koordinator_list:
    koordinator_data.append({
        "id": k.id,
        "kelompok": k.kelompok, 
        "koordinator": k.get_koordinator_list()
    })

print(f"Piramida akan dikirim ke template: {dict(piramida)}")
print(f"Koordinator data akan dikirim: {koordinator_data}")

if len(struktur_sorted) > 0 and len(koordinator_data) > 0:
    print("\n✅ Data lengkap, view seharusnya menampilkan kedua bagian")
elif len(struktur_sorted) > 0:
    print("\n⚠️ Hanya ada data Panitia Utama")
elif len(koordinator_data) > 0:
    print("\n⚠️ Hanya ada data Koordinator Kelompok")
else:
    print("\n❌ Tidak ada data apapun")
