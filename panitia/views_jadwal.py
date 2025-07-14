from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .helpers import get_akses  # Pastikan untuk mengimpor fungsi get_akses

@login_required
def jadwal(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Jadwal Kegiatan')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Jadwal'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Jadwal'})

    if request.user.username == 'siswa' and not request.user.is_superuser:
        return render(request, 'panitia/no_access.html', {'menu': 'Jadwal'})
    
    if 'jadwal1' not in request.session:
        request.session['jadwal1'] = []
    if 'jadwal2' not in request.session:
        request.session['jadwal2'] = []

    jadwal1 = request.session['jadwal1']
    jadwal2 = request.session['jadwal2']

    if request.method == 'POST':
        if 'tambah' in request.POST:
            hari = request.POST.get('hari')
            waktu = request.POST.get('waktu', '').strip()
            planA = request.POST.get('planA', '').strip()
            planB = request.POST.get('planB', '').strip()
            if hari and waktu and planA and planB:
                if hari == '1':
                    jadwal1.append({'waktu': waktu, 'planA': planA, 'planB': planB})
                    request.session['jadwal1'] = jadwal1
                elif hari == '2':
                    jadwal2.append({'waktu': waktu, 'planA': planA, 'planB': planB})
                    request.session['jadwal2'] = jadwal2
                return redirect('panitia:jadwal')

        for prefix in ['hapus', 'edit', 'up', 'down']:
            for hari in ['1', '2']:
                key = f'{prefix}{hari}'
                if key in request.POST:
                    idx = int(request.POST.get(key))
                    jadwal = jadwal1 if hari == '1' else jadwal2
                    if prefix == 'hapus' and 0 <= idx < len(jadwal):
                        jadwal.pop(idx)
                    elif prefix == 'edit' and 0 <= idx < len(jadwal):
                        request.session['edit_jadwal'] = {
                            'hari': int(hari), 'idx': idx, 'item': jadwal[idx]
                        }
                        return redirect('panitia:edit_jadwal')
                    elif prefix == 'up' and idx > 0:
                        jadwal[idx-1], jadwal[idx] = jadwal[idx], jadwal[idx-1]
                    elif prefix == 'down' and idx < len(jadwal)-1:
                        jadwal[idx+1], jadwal[idx] = jadwal[idx], jadwal[idx+1]
                    if hari == '1':
                        request.session['jadwal1'] = jadwal
                    else:
                        request.session['jadwal2'] = jadwal
                    return redirect('panitia:jadwal')

    return render(request, 'panitia/jadwal.html', {'jadwal1': jadwal1, 'jadwal2': jadwal2})


@login_required
def edit_jadwal(request):
    edit = request.session.get('edit_jadwal')
    if not edit:
        return redirect('panitia:jadwal')

    hari = edit['hari']
    idx = edit['idx']
    item = edit['item']

    if request.method == 'POST':
        waktu = request.POST.get('waktu', '').strip()
        planA = request.POST.get('planA', '').strip()
        planB = request.POST.get('planB', '').strip()
        if waktu and planA and planB:
            jadwal = request.session['jadwal1'] if hari == 1 else request.session['jadwal2']
            jadwal[idx] = {'waktu': waktu, 'planA': planA, 'planB': planB}
            if hari == 1:
                request.session['jadwal1'] = jadwal
            else:
                request.session['jadwal2'] = jadwal
            del request.session['edit_jadwal']
            return redirect('panitia:jadwal')

    return render(request, 'panitia/edit_jadwal.html', {'edit': edit})
