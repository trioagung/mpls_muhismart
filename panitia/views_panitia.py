from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.shortcuts import render, redirect
from .forms import PanitiaForm
from .helpers import get_akses
from .models import PanitiaUtama

# Dummy data koordinator kelompok
KOORDINATOR_KELOMPOK = []

## Hapus STRUKTUR_ORGANISASI dummy, gunakan database PanitiaPelaksana

TUGAS_KHUSUS = {}
TUGAS_UMUM = {
    "Penanggung Jawab": [
        "Mengawasi seluruh kegiatan panitia",
        "Memberikan arahan dan keputusan akhir",
        "Menjadi penanggung jawab utama kegiatan",
        "Menyelesaikan masalah strategis",
        "Menjadi penghubung dengan pihak eksternal"
    ],
    "Ketua Panitia": [
        "Mengkoordinasi seluruh panitia",
        "Membuat jadwal kegiatan",
        "Memimpin rapat panitia",
        "Mengawasi pelaksanaan tugas",
        "Menyusun laporan kegiatan"
    ],
    "Sekretaris": [
        "Mencatat hasil rapat",
        "Mengelola administrasi",
        "Membuat surat-menyurat",
        "Menyimpan dokumen penting",
        "Membantu ketua dalam administrasi"
    ],
    "Bendahara": [
        "Mengelola keuangan",
        "Membuat laporan keuangan",
        "Mencatat pemasukan dan pengeluaran",
        "Menyimpan bukti transaksi",
        "Membantu ketua dalam hal keuangan"
    ],
    "Pelaksana": [
        "Melaksanakan tugas teknis",
        "Membantu kelancaran acara",
        "Menyiapkan perlengkapan",
        "Mengatur peserta",
        "Membantu panitia lain"
    ],
}

def struktur_piramida(struktur):
    tree = {}
    lookup = {item['nama']: {**item, 'children': []} for item in struktur}
    for item in lookup.values():
        if item.get('parent') and item['parent'] in lookup:
            lookup[item['parent']]['children'].append(item)
        else:
            tree[item['nama']] = item
    return tree

@login_required
def struktur_organisasi(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Panitia Utama')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Panitia Utama'})
    struktur_sorted = list(PanitiaUtama.objects.all().order_by('kedudukan', 'jabatan'))
    piramida = defaultdict(list)
    for item in struktur_sorted:
        piramida[item.kedudukan].append({
            'nama': item.jabatan,
            'kedudukan': item.kedudukan,
            'anggota': item.anggota_list(),
            'tugas': '',
        })
    tree = struktur_piramida([{'nama': p.jabatan, 'kedudukan': p.kedudukan, 'parent': None, 'tugas': ''} for p in struktur_sorted])
    if request.method == "POST" and bisa_edit:
        if 'tambah_panitia' in request.POST:
            jabatan = request.POST.get('jabatan', '').strip()
            anggota = request.POST.get('anggota', '').strip()
            kedudukan = request.POST.get('kedudukan', '99').strip()
            try:
                kedudukan_int = int(kedudukan)
            except (ValueError, TypeError):
                kedudukan_int = 99
            if jabatan and anggota:
                PanitiaUtama.objects.create(jabatan=jabatan, anggota=anggota, kedudukan=kedudukan_int)
        elif 'hapus_panitia' in request.POST:
            jabatan = request.POST.get('hapus_panitia', '').strip()
            PanitiaUtama.objects.filter(jabatan=jabatan).delete()
        elif 'edit_panitia' in request.POST:
            jabatan = request.POST.get('edit_panitia', '').strip()
            anggota = request.POST.get('anggota_edit', '').strip()
            kedudukan = request.POST.get('kedudukan_edit', '99').strip()
            try:
                kedudukan_int = int(kedudukan)
            except (ValueError, TypeError):
                kedudukan_int = 99
            obj = PanitiaUtama.objects.filter(jabatan=jabatan).first()
            if obj and anggota:
                obj.anggota = anggota
                obj.kedudukan = kedudukan_int
                obj.save()
    edit_idx = None
    if request.method == "POST":
        if 'edit_panitia' in request.POST and not ('anggota_edit' in request.POST or 'kedudukan_edit' in request.POST):
            edit_idx = request.POST.get('edit_panitia')
    return render(request, 'panitia/struktur_organisasi.html', {
        "struktur": struktur_sorted,
        "piramida": dict(piramida),
        "struktur_piramida": tree,
        "edit_idx": edit_idx,
    })

@login_required
def tugas_panitia(request, jabatan):
    # Analisis jabatan secara fleksibel (case-insensitive, substring match)
    jabatan_lower = jabatan.lower()
    tugas_umum = None
    best_match = None
    best_score = 0
    for key in TUGAS_UMUM:
        key_lower = key.lower()
        # Skor kemiripan: jumlah kata yang cocok
        score = sum(1 for word in jabatan_lower.split() if word in key_lower)
        if key_lower in jabatan_lower or jabatan_lower in key_lower:
            score += 2
        if score > best_score:
            best_score = score
            best_match = key
    if best_match:
        tugas_umum = TUGAS_UMUM[best_match][:5]
    else:
        tugas_umum = ["Tidak ada tugas umum untuk jabatan ini."]
    tugas_khusus = TUGAS_KHUSUS.get(jabatan, [])
    if request.method == "POST":
        if 'tambah_tugas' in request.POST:
            tugas_baru = request.POST.get('tugas_khusus', '').strip()
            if tugas_baru:
                TUGAS_KHUSUS.setdefault(jabatan, []).append({"tugas": tugas_baru, "selesai": False})
        elif 'toggle_selesai' in request.POST:
            idx = int(request.POST.get('toggle_selesai'))
            if 0 <= idx < len(tugas_khusus):
                tugas_khusus[idx]["selesai"] = not tugas_khusus[idx]["selesai"]
        elif 'hapus_tugas' in request.POST:
            idx = int(request.POST.get('hapus_tugas'))
            if 0 <= idx < len(tugas_khusus):
                tugas_khusus.pop(idx)
        return redirect('panitia:tugas_panitia', jabatan=jabatan)
    return render(request, 'panitia/tugas_panitia.html', {
        "jabatan": jabatan,
        "tugas_umum": tugas_umum,
        "tugas_khusus": tugas_khusus,
    })

@login_required
def tambah_panitia(request):
    if request.method == 'POST':
        form = PanitiaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            anggota = data['anggota']
            try:
                kedudukan_int = int(data['kedudukan'])
            except (ValueError, TypeError):
                kedudukan_int = 99
            PanitiaUtama.objects.create(jabatan=data['jabatan'], anggota=anggota, kedudukan=kedudukan_int)
            return redirect('panitia:struktur_organisasi')
    else:
        form = PanitiaForm()
    return render(request, 'panitia/tambah_panitia.html', {"form": form})

@login_required
def hapus_panitia(request, jabatan):
    panitia = PanitiaUtama.objects.filter(jabatan=jabatan).first()
    if not panitia:
        return redirect('panitia:struktur_organisasi')
    if request.method == 'POST':
        panitia.delete()
        return redirect('panitia:struktur_organisasi')
    return render(request, 'panitia/hapus_panitia.html', {'panitia': panitia})

@login_required
def panitia_utama(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Panitia Utama')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Panitia Utama'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Panitia Utama'})
    return redirect('panitia:struktur_organisasi')
