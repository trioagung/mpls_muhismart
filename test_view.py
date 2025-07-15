import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpls.settings')
django.setup()

from panitia.models import PanitiaUtama
from collections import defaultdict

# Simulasi logic dari view struktur_organisasi
struktur_sorted = list(PanitiaUtama.objects.all().order_by('kedudukan', 'jabatan'))
print(f"Total data struktur: {len(struktur_sorted)}")

piramida = defaultdict(list)
for item in struktur_sorted:
    print(f"Processing: {item.jabatan} - kedudukan: {item.kedudukan}")
    print(f"Anggota list: {item.anggota_list()}")
    
    piramida[item.kedudukan].append({
        'nama': item.jabatan,
        'kedudukan': item.kedudukan,
        'anggota': item.anggota_list(),
        'tugas': '',
    })

print(f"\nPiramida structure:")
for kedudukan, items in piramida.items():
    print(f"Kedudukan {kedudukan}:")
    for item in items:
        print(f"  - {item['nama']}: {item['anggota']}")

# Test template context
context = {
    "struktur": struktur_sorted,
    "piramida": dict(piramida),
    "bisa_lihat": True,
    "bisa_edit": True,
}

print(f"\nTemplate context keys: {list(context.keys())}")
print(f"Piramida in context: {context['piramida']}")
