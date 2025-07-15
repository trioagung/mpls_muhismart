from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .helpers import get_akses  # Pastikan untuk mengimpor fungsi get_akses
from .models import Jadwal

@login_required
def jadwal(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Jadwal Kegiatan')
    
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Jadwal'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Jadwal'})

    if request.user.username == 'siswa' and not request.user.is_superuser:
        return render(request, 'panitia/no_access.html', {'menu': 'Jadwal'})
    
    # Ambil data jadwal dari database
    jadwal1_db = Jadwal.objects.filter(hari=1).order_by('urutan')
    jadwal2_db = Jadwal.objects.filter(hari=2).order_by('urutan')
    
    # Convert ke format yang sama dengan session
    jadwal1 = [{'waktu': j.waktu, 'planA': j.plan_a, 'planB': j.plan_b} for j in jadwal1_db]
    jadwal2 = [{'waktu': j.waktu, 'planA': j.plan_a, 'planB': j.plan_b} for j in jadwal2_db]

    if request.method == 'POST':
        if 'tambah' in request.POST:
            hari = request.POST.get('hari')
            waktu = request.POST.get('waktu', '').strip()
            planA = request.POST.get('planA', '').strip()
            planB = request.POST.get('planB', '').strip()
            if hari and waktu and planA and planB:
                hari_int = int(hari)
                # Hitung urutan terakhir untuk hari ini
                last_urutan = Jadwal.objects.filter(hari=hari_int).count()
                # Simpan ke database
                Jadwal.objects.create(
                    hari=hari_int,
                    waktu=waktu,
                    plan_a=planA,
                    plan_b=planB,
                    urutan=last_urutan
                )
                return redirect('panitia:jadwal')

        for prefix in ['hapus', 'edit', 'up', 'down']:
            for hari in ['1', '2']:
                key = f'{prefix}{hari}'
                if key in request.POST:
                    idx = int(request.POST.get(key))
                    hari_int = int(hari)
                    jadwal_items = Jadwal.objects.filter(hari=hari_int).order_by('urutan')
                    
                    if prefix == 'hapus' and 0 <= idx < jadwal_items.count():
                        # Hapus item dari database
                        item_to_delete = jadwal_items[idx]
                        item_to_delete.delete()
                        # Update urutan untuk item setelahnya
                        for i, item in enumerate(Jadwal.objects.filter(hari=hari_int).order_by('urutan')):
                            item.urutan = i
                            item.save()
                            
                    elif prefix == 'edit' and 0 <= idx < jadwal_items.count():
                        item_to_edit = jadwal_items[idx]
                        request.session['edit_jadwal'] = {
                            'id': item_to_edit.pk,
                            'hari': hari_int, 
                            'idx': idx, 
                            'item': {
                                'waktu': item_to_edit.waktu,
                                'planA': item_to_edit.plan_a,
                                'planB': item_to_edit.plan_b
                            }
                        }
                        return redirect('panitia:edit_jadwal')
                        
                    elif prefix == 'up' and idx > 0 and idx < jadwal_items.count():
                        # Tukar urutan dengan item sebelumnya
                        item1 = jadwal_items[idx-1]
                        item2 = jadwal_items[idx]
                        item1.urutan, item2.urutan = item2.urutan, item1.urutan
                        item1.save()
                        item2.save()
                        
                    elif prefix == 'down' and idx < jadwal_items.count()-1:
                        # Tukar urutan dengan item setelahnya
                        item1 = jadwal_items[idx]
                        item2 = jadwal_items[idx+1]
                        item1.urutan, item2.urutan = item2.urutan, item1.urutan
                        item1.save()
                        item2.save()
                    
                    return redirect('panitia:jadwal')

    return render(request, 'panitia/jadwal.html', {
        'jadwal1': jadwal1, 
        'jadwal2': jadwal2,
        'bisa_lihat': bisa_lihat,
        'bisa_edit': bisa_edit,
    })


@login_required
def edit_jadwal(request):
    edit = request.session.get('edit_jadwal')
    if not edit:
        return redirect('panitia:jadwal')

    jadwal_id = edit.get('id')
    item = edit['item']

    if request.method == 'POST':
        waktu = request.POST.get('waktu', '').strip()
        planA = request.POST.get('planA', '').strip()
        planB = request.POST.get('planB', '').strip()
        if waktu and planA and planB:
            try:
                jadwal_obj = Jadwal.objects.get(pk=jadwal_id)
                jadwal_obj.waktu = waktu
                jadwal_obj.plan_a = planA
                jadwal_obj.plan_b = planB
                jadwal_obj.save()
                del request.session['edit_jadwal']
                return redirect('panitia:jadwal')
            except Jadwal.DoesNotExist:
                # Jika objek tidak ditemukan, redirect kembali
                del request.session['edit_jadwal']
                return redirect('panitia:jadwal')

    return render(request, 'panitia/edit_jadwal.html', {'edit': edit})
