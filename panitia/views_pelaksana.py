from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Kelompok, Anggota

@login_required
def pelaksana(request):
    daftar_kelompok = Kelompok.objects.all()

    if request.method == 'POST':
        for kelompok in daftar_kelompok:
            pelaksana_nama = request.POST.get(f'pelaksana_{kelompok.id}')
            if pelaksana_nama:
                anggota = Anggota.objects.filter(nama=pelaksana_nama, kelompok=kelompok).first()
                if anggota:
                    kelompok.pelaksana = anggota
                    kelompok.save()
        return redirect('panitia:pelaksana')

    return render(request, 'panitia/pelaksana.html', {
        'daftar_kelompok': daftar_kelompok,
        'anggota_kelompok': {
            kelompok.id: Anggota.objects.filter(kelompok=kelompok)
            for kelompok in daftar_kelompok
        }
    })

@login_required
def tugas_pelaksana(request, jabatan):
    from .views_panitia import TUGAS_UMUM, TUGAS_KHUSUS
    jabatan_lower = jabatan.lower()
    tugas_umum = None
    best_match = None
    best_score = 0
    for key in TUGAS_UMUM:
        key_lower = key.lower()
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
        return redirect('panitia:tugas_pelaksana', jabatan=jabatan)
    return render(request, 'panitia/tugas_pelaksana.html', {
        "jabatan": jabatan,
        "tugas_umum": tugas_umum,
        "tugas_khusus": tugas_khusus,
    })
