from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .helpers import get_akses

@login_required
def surat(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Surat-surat')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Surat-surat'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Surat-surat'})
    if 'surat_list' not in request.session:
        request.session['surat_list'] = []
    surat_list = request.session['surat_list']
    if request.method == 'POST' and 'tambah_surat' in request.POST:
        nama = request.POST.get('nama_surat', '').strip()
        file = request.FILES.get('file_surat')
        if nama and file:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'surat'))
            filename = fs.save(file.name, file)
            url = fs.url('surat/' + filename)
            surat_list.append({'nama': nama, 'url': url})
            request.session['surat_list'] = surat_list
            return redirect('panitia:surat')
    return render(request, 'panitia/surat.html', {
        'surat_list': surat_list,
        'bisa_lihat': bisa_lihat,
        'bisa_edit': bisa_edit,
    })
