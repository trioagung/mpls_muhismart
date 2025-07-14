from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .helpers import get_akses
from .forms_pengumuman import PengumumanForm
from .models import Pengumuman


@login_required
def pengumuman(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Pengumuman')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Pengumuman'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Pengumuman'})

    pengumuman_list = Pengumuman.objects.order_by('-waktu')

    # Proses edit
    if request.method == 'POST':
        if 'hapus' in request.POST:
            Pengumuman.objects.filter(id=int(request.POST['hapus'])).delete()
            return redirect('panitia:pengumuman')
        if 'edit_pengumuman' in request.POST:
            pengumuman_id = int(request.POST['edit_pengumuman'])
            obj = Pengumuman.objects.filter(id=pengumuman_id).first()
            if obj:
                form = PengumumanForm(initial={'judul': obj.judul, 'isi': obj.isi})
                return render(request, 'panitia/edit_pengumuman.html', {
                    'form': form,
                    'edit_idx': pengumuman_id,
                })
        if 'simpan_edit' in request.POST:
            pengumuman_id = int(request.POST.get('edit_idx', 0))
            obj = Pengumuman.objects.filter(id=pengumuman_id).first()
            form = PengumumanForm(request.POST)
            if obj and form.is_valid():
                cd = form.cleaned_data
                obj.judul = cd.get('judul', obj.judul)
                obj.isi = cd.get('isi', obj.isi)
                obj.save()
                return redirect('panitia:pengumuman')
        # Tambah pengumuman
        form = PengumumanForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Pengumuman.objects.create(judul=cd.get('judul', ''), isi=cd.get('isi', ''))
            return redirect('panitia:pengumuman')
    else:
        form = PengumumanForm()
    return render(request, 'panitia/pengumuman.html', {
        'pengumuman_list': pengumuman_list,
        'form': form,
        'bisa_lihat': bisa_lihat,
        'bisa_edit': bisa_edit,
    })
