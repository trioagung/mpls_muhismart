from django.contrib.auth.decorators import login_required

@login_required
def edit_larangan(request, id):
    barang = LaranganBarang.objects.filter(id=id).first()
    if not barang:
        return redirect('panitia:logistik')

    if request.method == 'POST':
        nama = request.POST.get('nama', '').strip()
        if nama:
            barang.nama = nama
            barang.save()
            return redirect('panitia:logistik')
        if 'batal' in request.POST:
            return redirect('panitia:logistik')

    return render(request, 'panitia/edit_larangan.html', {'edit': barang})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .helpers import get_akses
from .models import BarangLogistik, LaranganBarang

@login_required
def logistik(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Logistik')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Logistik'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Logistik'})

    # Ambil data dari database
    logistik_pribadi = BarangLogistik.objects.filter(jenis='pribadi').order_by('-waktu')
    logistik_kelompok = BarangLogistik.objects.filter(jenis='kelompok').order_by('-waktu')
    barang_larangan = LaranganBarang.objects.order_by('-waktu')

    if request.method == 'POST':
        # Tambah logistik pribadi
        if 'tambah_pribadi' in request.POST:
            nama = request.POST.get('logistik_pribadi', '').strip()
            if nama:
                BarangLogistik.objects.create(nama=nama, jenis='pribadi')
            return redirect('panitia:logistik')
        # Tambah logistik kelompok
        if 'tambah_kelompok' in request.POST:
            nama = request.POST.get('logistik_kelompok', '').strip()
            if nama:
                BarangLogistik.objects.create(nama=nama, jenis='kelompok')
            return redirect('panitia:logistik')
        # Hapus logistik pribadi
        if 'hapus_pribadi' in request.POST:
            id_hapus = request.POST.get('hapus_pribadi')
            BarangLogistik.objects.filter(id=id_hapus, jenis='pribadi').delete()
            return redirect('panitia:logistik')
        # Hapus logistik kelompok
        if 'hapus_kelompok' in request.POST:
            id_hapus = request.POST.get('hapus_kelompok')
            BarangLogistik.objects.filter(id=id_hapus, jenis='kelompok').delete()
            return redirect('panitia:logistik')
        # Edit logistik pribadi
        if 'edit_pribadi' in request.POST:
            id_edit = request.POST.get('edit_pribadi')
            barang = BarangLogistik.objects.filter(id=id_edit, jenis='pribadi').first()
            if barang:
                return redirect(f"/panitia/logistik/edit/{barang.id}/?jenis=pribadi")
        # Edit logistik kelompok
        if 'edit_kelompok' in request.POST:
            id_edit = request.POST.get('edit_kelompok')
            barang = BarangLogistik.objects.filter(id=id_edit, jenis='kelompok').first()
            if barang:
                return redirect(f"/panitia/logistik/edit/{barang.id}/?jenis=kelompok")
        # Tambah barang larangan
        if 'tambah_larangan' in request.POST:
            nama = request.POST.get('barang_larangan', '').strip()
            if nama:
                LaranganBarang.objects.create(nama=nama)
            return redirect('panitia:logistik')
        # Hapus barang larangan
        if 'hapus_larangan' in request.POST:
            id_hapus = request.POST.get('hapus_larangan')
            LaranganBarang.objects.filter(id=id_hapus).delete()
            return redirect('panitia:logistik')
        # Edit barang larangan
        if 'edit_larangan' in request.POST:
            id_edit = request.POST.get('edit_larangan')
            barang = LaranganBarang.objects.filter(id=id_edit).first()
            if barang:
                request.session['edit_larangan_id'] = barang.id
                return redirect('panitia:edit_larangan')

    return render(request, 'panitia/logistik.html', {
        'logistik_pribadi': logistik_pribadi,
        'logistik_kelompok': logistik_kelompok,
        'barang_larangan': barang_larangan,
        'bisa_lihat': bisa_lihat,
        'bisa_edit': bisa_edit,
    })

    if request.method == 'POST':
        if 'tambah_barang' in request.POST:
            nama = request.POST.get('nama')
            jumlah = request.POST.get('jumlah')
            if nama and jumlah.isdigit():
                barang = {'nama': nama, 'jumlah': int(jumlah)}
                logistik.append(barang)
                request.session['logistik'] = logistik
            return redirect('panitia:logistik')

        if 'hapus_barang' in request.POST:
            id_barang = request.POST.get('hapus_barang')
            if id_barang.isdigit() and 0 <= int(id_barang) < len(logistik):
                logistik.pop(int(id_barang))
                request.session['logistik'] = logistik
            return redirect('panitia:logistik')

        if 'tambah_larangan' in request.POST:
            nama = request.POST.get('nama')
            if nama:
                larangan.append(nama)
                request.session['larangan'] = larangan
            return redirect('panitia:logistik')

        if 'hapus_larangan' in request.POST:
            id_larangan = request.POST.get('hapus_larangan')
            if id_larangan.isdigit() and 0 <= int(id_larangan) < len(larangan):
                larangan.pop(int(id_larangan))
                request.session['larangan'] = larangan
            return redirect('panitia:logistik')

        if 'edit_barang_id' in request.POST:
            id_edit = request.POST.get('edit_barang_id')
            if id_edit.isdigit() and 0 <= int(id_edit) < len(logistik):
                barang = logistik[int(id_edit)]
                request.session['edit_barang'] = {'id': id_edit, 'nama': barang['nama'], 'jumlah': barang['jumlah']}
                return redirect('panitia:edit_logistik')

    return render(request, 'panitia/logistik.html', {'logistik': logistik, 'larangan': larangan})


@login_required
def edit_logistik(request, id):
    jenis = request.GET.get('jenis', 'pribadi')
    barang = BarangLogistik.objects.filter(id=id).first()
    if not barang:
        return redirect('panitia:logistik')

    if request.method == 'POST':
        nama = request.POST.get('nama', '').strip()
        jumlah = request.POST.get('jumlah', '').strip()
        if nama:
            barang.nama = nama
            if jumlah.isdigit():
                barang.jumlah = int(jumlah)
            barang.save()
            return redirect('panitia:logistik')
        if 'batal' in request.POST:
            return redirect('panitia:logistik')

    return render(request, 'panitia/edit_logistik.html', {'edit': barang, 'jenis': jenis})

    if request.method == 'POST':
        nama = request.POST.get('nama')
        jumlah = request.POST.get('jumlah')
        if nama and jumlah.isdigit():
            barang = request.session['logistik'][int(edit['id'])]
            if barang:
                barang['nama'] = nama
                barang['jumlah'] = int(jumlah)
                request.session.modified = True
                return redirect('panitia:logistik')

    return render(request, 'panitia/edit_logistik.html', {'edit': edit})
