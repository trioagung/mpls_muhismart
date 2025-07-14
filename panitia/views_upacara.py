from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .helpers import get_akses

TUGAS_UMUM_UPACARA = {
    "Pemimpin Upacara": [
        "Memimpin jalannya upacara dengan tegas dan khidmat.",
        "Memberikan aba-aba kepada peserta upacara.",
        "Menjaga ketertiban dan kelancaran upacara.",
        "Berkoordinasi dengan petugas lain sebelum upacara dimulai.",
        "Menyampaikan laporan pelaksanaan upacara kepada pembina."
    ],
    # ...tambahkan jabatan lain sesuai kebutuhan...
}
TUGAS_KHUSUS_UPACARA = {}

@login_required
def tugas_upacara(request, jabatan):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Upacara')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Upacara'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Upacara'})
    
    tugas_umum = TUGAS_UMUM_UPACARA.get(jabatan, [
        "Melaksanakan tugas sesuai arahan pemimpin upacara.",
        "Membantu kelancaran upacara.",
        "Menyiapkan perlengkapan upacara.",
        "Mengatur peserta sesuai tugasnya.",
        "Bertanggung jawab atas tugas yang diberikan."
    ])
    tugas_khusus = TUGAS_KHUSUS_UPACARA.get(jabatan, [])
    if request.method == "POST":
        if 'tambah_tugas' in request.POST:
            tugas_baru = request.POST.get('tugas_khusus', '').strip()
            if tugas_baru:
                TUGAS_KHUSUS_UPACARA.setdefault(jabatan, []).append({"tugas": tugas_baru, "selesai": False})
        elif 'toggle_selesai' in request.POST:
            idx = int(request.POST.get('toggle_selesai'))
            if 0 <= idx < len(tugas_khusus):
                tugas_khusus[idx]["selesai"] = not tugas_khusus[idx]["selesai"]
        elif 'hapus_tugas' in request.POST:
            idx = int(request.POST.get('hapus_tugas'))
            if 0 <= idx < len(tugas_khusus):
                tugas_khusus.pop(idx)
        return redirect('panitia:tugas_upacara', jabatan=jabatan)
    return render(request, 'panitia/tugas_upacara.html', {
        "jabatan": jabatan,
        "tugas_umum": tugas_umum,
        "tugas_khusus": tugas_khusus,
    })
