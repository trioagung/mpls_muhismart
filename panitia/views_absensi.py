
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Kelompok, Anggota, Agenda, Absensi
from .helpers import get_akses
import json

@login_required
def absensi(request):
    # Cek permission user untuk menu Absensi
    bisa_lihat, bisa_edit = get_akses(request.user, 'Absensi')
    
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Absensi'})
    
    # Jika POST request tapi user tidak punya permission edit
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Absensi'})
    # Ambil data kelompok dari model daftar kelompok 
    daftar_kelompok = []
    for kel in Kelompok.objects.all():
        daftar_kelompok.append({
            'nama_kelompok': kel.nama,
        })
    
    # Ambil kelompok yang sudah ditambahkan untuk absensi
    kelompok_absen = []
    for kel in Kelompok.objects.all():
        anggota_list = []
        for anggota in Anggota.objects.filter(kelompok=kel):
            anggota_list.append({
                'nama': anggota.nama,
                'ketua': anggota.is_ketua
            })
        if anggota_list:  # hanya tampilkan kelompok yang ada anggotanya
            kelompok_absen.append({
                'nama': kel.nama,
                'anggota': anggota_list
            })
    
    # Ambil daftar agenda dengan ID
    agenda_list = []
    for agenda in Agenda.objects.all().order_by('urutan'):
        agenda_list.append({
            'id': agenda.id,
            'nama': agenda.nama
        })
    
    # Buat data absensi
    absensi_data = {}
    for kel in Kelompok.objects.all():
        absensi_data[kel.nama] = {}
        for anggota in Anggota.objects.filter(kelompok=kel):
            absensi_data[kel.nama][anggota.nama] = {}
            for agenda_item in agenda_list:
                agenda = Agenda.objects.get(id=agenda_item['id'])
                absensi_obj = Absensi.objects.filter(anggota=anggota, agenda=agenda).first()
                absensi_data[kel.nama][anggota.nama][agenda_item['nama']] = absensi_obj.hadir if absensi_obj else False

    if request.method == 'POST':
        # Handle tambah kelompok dari daftar
        if 'tambah_kelompok' in request.POST:
            nama_kelompok = request.POST.get('kelompok_dari_daftar', '').strip()
            if nama_kelompok:
                # Kelompok sudah ada di database, tidak perlu create lagi
                pass
            return redirect('panitia:absensi')
        
        # Handle tambah agenda
        if 'tambah_agenda' in request.POST:
            nama_agenda = request.POST.get('nama_agenda', '').strip()
            if nama_agenda and not Agenda.objects.filter(nama=nama_agenda).exists():
                max_urutan = Agenda.objects.count()
                Agenda.objects.create(nama=nama_agenda, urutan=max_urutan)
            return redirect('panitia:absensi')
        
        # Handle edit agenda
        if 'edit_agenda' in request.POST:
            print("Edit agenda request received")
            agenda_id = request.POST.get('agenda_id')
            nama_baru = request.POST.get('nama_agenda_baru', '').strip()
            print(f"Agenda ID: {agenda_id}, Nama baru: {nama_baru}")
            if agenda_id and nama_baru:
                try:
                    agenda = Agenda.objects.get(id=agenda_id)
                    print(f"Found agenda: {agenda.nama}")
                    if not Agenda.objects.filter(nama=nama_baru).exclude(id=agenda_id).exists():
                        old_name = agenda.nama
                        agenda.nama = nama_baru
                        agenda.save()
                        print(f"Successfully updated agenda from '{old_name}' to '{nama_baru}'")
                    else:
                        print(f"Agenda with name '{nama_baru}' already exists")
                except Agenda.DoesNotExist:
                    print(f"Agenda with ID {agenda_id} not found")
            else:
                print("Missing agenda_id or nama_baru")
            return redirect('panitia:absensi')
        
        # Handle hapus agenda
        if 'hapus_agenda' in request.POST:
            agenda_id = request.POST.get('agenda_id')
            if agenda_id:
                try:
                    agenda = Agenda.objects.get(id=agenda_id)
                    # Hapus semua data absensi terkait agenda ini
                    Absensi.objects.filter(agenda=agenda).delete()
                    # Hapus agenda
                    agenda.delete()
                except Agenda.DoesNotExist:
                    pass
            return redirect('panitia:absensi')
        
        # Handle absensi checkbox
        for key in request.POST:
            if key.startswith('absen_'):
                _, nama_kelompok, nama_anggota, nama_agenda = key.split('_', 3)
                kel = Kelompok.objects.filter(nama=nama_kelompok).first()
                anggota = Anggota.objects.filter(nama=nama_anggota, kelompok=kel).first()
                agenda = Agenda.objects.filter(nama=nama_agenda).first()
                checked = request.POST.get(key) == 'on'
                if anggota and agenda:
                    absensi_obj, created = Absensi.objects.get_or_create(anggota=anggota, agenda=agenda)
                    absensi_obj.hadir = checked
                    absensi_obj.save()
        
        # Handle swap agenda order via AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST.get('agenda_order'):
            order = json.loads(request.POST['agenda_order'])
            for idx, nama_agenda in enumerate(order):
                Agenda.objects.filter(nama=nama_agenda).update(urutan=idx)
            return JsonResponse({'status': 'ok'})
        
        return redirect('panitia:absensi')

    return render(request, 'panitia/absensi.html', {
        'daftar_kelompok': daftar_kelompok,
        'kelompok_absen': kelompok_absen,
        'agenda_list': agenda_list,
        'absensi_data': absensi_data,
        'bisa_edit': bisa_edit,
    })
