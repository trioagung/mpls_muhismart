from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def menu_ipm(request):
    from .helpers import get_akses
    akses_pelaksana, _ = get_akses(request.user, 'Panitia Utama')
    akses_koordinator, _ = get_akses(request.user, 'Daftar Kelompok')
    akses_upacara, _ = get_akses(request.user, 'Upacara')
    return render(request, 'panitia/menu_ipm.html', {
        "akses_pelaksana": akses_pelaksana,
        "akses_koordinator": akses_koordinator,
        "akses_upacara": akses_upacara,
    })

@login_required
def panitia_pelaksana(request):
    from .forms_pelaksana import PanitiaPelaksanaForm
    from .models import PanitiaPelaksana
    if request.method == 'POST':
        form = PanitiaPelaksanaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            anggota = data['anggota']
            try:
                kedudukan_int = int(data['kedudukan'])
            except (ValueError, TypeError):
                kedudukan_int = 99
            PanitiaPelaksana.objects.create(jabatan=data['jabatan'], anggota=anggota, kedudukan=kedudukan_int)
            return redirect('panitia:panitia_pelaksana')
    else:
        form = PanitiaPelaksanaForm()
    if request.method == 'POST' and 'hapus' in request.POST:
        jabatan = request.POST.get('hapus')
        PanitiaPelaksana.objects.filter(jabatan=jabatan).delete()
        return redirect('panitia:panitia_pelaksana')
    panitia_sorted = PanitiaPelaksana.objects.all().order_by('kedudukan', 'jabatan')
    from .helpers import get_akses
    bisa_lihat, bisa_edit = get_akses(request.user, 'Panitia Pelaksana')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Panitia Pelaksana'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Panitia Pelaksana'})
    return render(request, 'panitia/pelaksana.html', {
        "panitia_pelaksana": panitia_sorted,
        "form": form,
        "bisa_lihat": bisa_lihat,
        "bisa_edit": bisa_edit,
    })

@login_required
def koordinator_kelompok(request):
    from .helpers import get_akses
    bisa_lihat, bisa_edit = get_akses(request.user, 'Koordinator Kelompok')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Koordinator Kelompok'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Koordinator Kelompok'})
    if 'koordinator_kelompok_ipm' not in request.session:
        request.session['koordinator_kelompok_ipm'] = []
    data = request.session['koordinator_kelompok_ipm']
    if request.method == 'POST' and bisa_edit:
        if 'tambah_koordinator' in request.POST:
            kelompok = request.POST.get('kelompok', '').strip()
            koordinator = [k.strip() for k in request.POST.get('koordinator', '').splitlines() if k.strip()]
            if kelompok and koordinator:
                data.append({"kelompok": kelompok, "koordinator": koordinator})
                request.session['koordinator_kelompok_ipm'] = data
        elif 'hapus_koordinator' in request.POST:
            idx = int(request.POST.get('hapus_koordinator'))
            if 0 <= idx < len(data):
                data.pop(idx)
                request.session['koordinator_kelompok_ipm'] = data
        elif 'edit_koordinator' in request.POST:
            idx = int(request.POST.get('edit_koordinator'))
            kelompok = request.POST.get('kelompok_edit', '').strip()
            koordinator = [k.strip() for k in request.POST.get('koordinator_edit', '').splitlines() if k.strip()]
            if kelompok and koordinator and 0 <= idx < len(data):
                data[idx] = {"kelompok": kelompok, "koordinator": koordinator}
                request.session['koordinator_kelompok_ipm'] = data
    edit_idx = None
    if request.method == 'POST':
        if 'edit_koordinator' in request.POST and not ('kelompok_edit' in request.POST or 'koordinator_edit' in request.POST):
            edit_idx = request.POST.get('edit_koordinator')
    return render(request, 'panitia/koordinator_kelompok.html', {
        "koordinator_kelompok": data,
        "edit_idx": edit_idx,
        "bisa_lihat": bisa_lihat,
        "bisa_edit": bisa_edit,
    })

@login_required
def petugas_upacara(request):
    from .forms_upacara import PetugasUpacaraForm
    from .models import PanitiaPelaksana
    from .helpers import get_akses
    bisa_lihat, bisa_edit = get_akses(request.user, 'Petugas Upacara')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Petugas Upacara'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Petugas Upacara'})
    if request.method == 'POST' and bisa_edit:
        form = PetugasUpacaraForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            anggota = data['anggota']
            try:
                kedudukan_int = int(data['kedudukan'])
            except (ValueError, TypeError):
                kedudukan_int = 99
            PanitiaPelaksana.objects.create(jabatan=data['jabatan'], anggota=anggota, kedudukan=kedudukan_int)
            return redirect('panitia:petugas_upacara')
    else:
        form = PetugasUpacaraForm()
    if request.method == 'POST' and 'hapus' in request.POST and bisa_edit:
        jabatan = request.POST.get('hapus')
        PanitiaPelaksana.objects.filter(jabatan=jabatan).delete()
        return redirect('panitia:petugas_upacara')
    petugas_sorted = PanitiaPelaksana.objects.all().order_by('kedudukan', 'jabatan')
    return render(request, 'panitia/petugas_upacara.html', {
        "petugas_upacara": petugas_sorted,
        "form": form,
        "bisa_lihat": bisa_lihat,
        "bisa_edit": bisa_edit,
    })
