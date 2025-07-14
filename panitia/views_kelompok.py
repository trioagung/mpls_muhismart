from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db import models
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import io, xlsxwriter
from .models import Kelompok, Anggota, Agenda, Absensi
from .helpers import get_akses
try:
    from .views import import_absensi_session_to_db
except ImportError:
    def import_absensi_session_to_db(request):
        pass

@login_required
def absensi(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Daftar Kelompok')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Daftar Kelompok'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Daftar Kelompok'})
    import_absensi_session_to_db(request)
    daftar_kelompok = list(Kelompok.objects.all())
    kelompok_absen = []
    for kel in daftar_kelompok:
        anggota = list(Anggota.objects.filter(kelompok=kel))
        kelompok_absen.append({'nama': kel.nama, 'anggota': [{'nama': a.nama, 'ketua': a.is_ketua} for a in anggota]})
    agenda_objs = Agenda.objects.all().order_by('urutan', 'id')
    agenda_list = [a.nama for a in agenda_objs]
    absensi_data = {}
    for kel in daftar_kelompok:
        absensi_data[kel.nama] = {}
        for a in Anggota.objects.filter(kelompok=kel):
            absensi_data[kel.nama][a.nama] = {}
            for ag in agenda_list:
                hadir = Absensi.objects.filter(anggota=a, agenda__nama=ag).first()
                absensi_data[kel.nama][a.nama][ag] = hadir.hadir if hadir else False
    if request.method == 'POST':
        if 'tambah_kelompok' in request.POST:
            return redirect('panitia:absensi')
        if 'tambah_agenda' in request.POST:
            nama_agenda = request.POST.get('nama_agenda')
            if nama_agenda and not Agenda.objects.filter(nama=nama_agenda).exists():
                max_urutan = Agenda.objects.aggregate(models.Max('urutan'))['urutan__max'] or 0
                Agenda.objects.create(nama=nama_agenda, urutan=max_urutan+1)
            return redirect('panitia:absensi')
        for key in request.POST:
            if key.startswith('absen_'):
                _, nama_kelompok, nama_anggota, nama_agenda = key.split('_', 3)
                kel = Kelompok.objects.filter(nama=nama_kelompok).first()
                anggota = Anggota.objects.filter(nama=nama_anggota, kelompok=kel).first()
                agenda = Agenda.objects.filter(nama=nama_agenda).first()
                checked = request.POST.get(key) == 'on'
                if anggota and agenda:
                    ab, created = Absensi.objects.get_or_create(anggota=anggota, agenda=agenda)
                    ab.hadir = checked
                    ab.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST.get('agenda_order'):
            import json
            order = json.loads(request.POST['agenda_order'])
            for idx, nama_agenda in enumerate(order):
                Agenda.objects.filter(nama=nama_agenda).update(urutan=idx)
            return JsonResponse({'status': 'ok'})
        return redirect('panitia:absensi')
    return render(request, 'panitia/absensi.html', {
        'daftar_kelompok': [{'nama_kelompok': k.nama} for k in daftar_kelompok],
        'kelompok_absen': kelompok_absen,
        'agenda_list': agenda_list,
        'absensi_data': absensi_data,
    })

@login_required
def download_absensi_excel(request):
    daftar_kelompok = list(Kelompok.objects.all())
    agenda_list = list(Agenda.objects.values_list('nama', flat=True))
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Absensi')
    row = 0
    col = 0
    worksheet.write(row, col, 'Kelompok')
    worksheet.write(row, col+1, 'Nama Anggota')
    for idx, agenda in enumerate(agenda_list):
        worksheet.write(row, col+2+idx, agenda)
    row += 1
    for kel in daftar_kelompok:
        anggota_list = Anggota.objects.filter(kelompok=kel)
        for anggota in anggota_list:
            worksheet.write(row, col, kel.nama)
            worksheet.write(row, col+1, anggota.nama)
            for idx, agenda in enumerate(agenda_list):
                ag = Agenda.objects.filter(nama=agenda).first()
                hadir = Absensi.objects.filter(anggota=anggota, agenda=ag).first()
                worksheet.write(row, col+2+idx, '✓' if hadir and hadir.hadir else '')
            row += 1
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=absensi.xlsx'
    return response

@login_required
def download_absensi_pdf(request):
    daftar_kelompok = list(Kelompok.objects.all())
    agenda_list = list(Agenda.objects.values_list('nama', flat=True))
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    y = height - 40
    p.setFont('Helvetica-Bold', 16)
    p.drawCentredString(width/2, y, 'Daftar Absensi')
    y -= 30
    p.setFont('Helvetica', 10)
    for kel in daftar_kelompok:
        p.setFont('Helvetica-Bold', 12)
        p.drawString(40, y, f"Kelompok: {kel.nama}")
        y -= 18
        p.setFont('Helvetica-Bold', 10)
        x = 40
        p.drawString(x, y, 'No')
        x += 30
        p.drawString(x, y, 'Nama Anggota')
        x += 120
        for agenda in agenda_list:
            p.drawString(x, y, agenda[:15])
            x += 70
        y -= 15
        p.setFont('Helvetica', 10)
        anggota_list = Anggota.objects.filter(kelompok=kel)
        for idx, anggota in enumerate(anggota_list, 1):
            x = 40
            p.drawString(x, y, str(idx))
            x += 30
            p.drawString(x, y, anggota.nama)
            x += 120
            for agenda in agenda_list:
                ag = Agenda.objects.filter(nama=agenda).first()
                hadir = Absensi.objects.filter(anggota=anggota, agenda=ag).first()
                p.drawString(x, y, '✓' if hadir and hadir.hadir else '-')
                x += 70
            y -= 15
            if y < 60:
                p.showPage()
                y = height - 40
        y -= 10
        if y < 60:
            p.showPage()
            y = height - 40
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=absensi.pdf'
    return response

@login_required
def daftar_kelompok(request):
    from .models import Kelompok, Anggota
    
    # Tambahkan pengecekan akses
    bisa_lihat, bisa_edit = get_akses(request.user, 'Daftar Kelompok')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Daftar Kelompok'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Daftar Kelompok'})
    
    kelompok_list = Kelompok.objects.all()
    if request.method == 'POST' and bisa_edit:
        if 'hapus_kelompok' in request.POST:
            nama_kelompok = request.POST.get('hapus_kelompok')
            Kelompok.objects.filter(nama=nama_kelompok).delete()
            return redirect('panitia:daftar_kelompok')
        elif 'tambah_kelompok' in request.POST:
            nama_kelompok = request.POST.get('nama_kelompok', '').strip()
            ketua = request.POST.get('ketua', '').strip()
            koordinator = request.POST.get('koordinator', '').strip()
            anggota = request.POST.get('anggota', '').strip()
            if nama_kelompok:
                kel = Kelompok.objects.create(nama=nama_kelompok, ketua=ketua)
                if koordinator:
                    Anggota.objects.create(nama=koordinator, kelompok=kel, is_ketua=True)
                if anggota:
                    for a in anggota.splitlines():
                        a = a.strip()
                        if a:
                            Anggota.objects.create(nama=a, kelompok=kel)
                return redirect('panitia:daftar_kelompok')
        elif 'detail_kelompok' in request.POST:
            nama_kelompok = request.POST.get('detail_kelompok')
            try:
                kelompok = Kelompok.objects.get(nama=nama_kelompok)
                anggota_list = Anggota.objects.filter(kelompok=kelompok, is_ketua=False)
                koordinator_list = Anggota.objects.filter(kelompok=kelompok, is_ketua=True)
            except Kelompok.DoesNotExist:
                kelompok = None
                anggota_list = []
                koordinator_list = []
            return render(request, 'panitia/detail_kelompok.html', {
                'kelompok': kelompok,
                'anggota_list': anggota_list,
                'koordinator_list': koordinator_list,
            })
        elif 'edit_kelompok' in request.POST:
            nama_kelompok = request.POST.get('edit_kelompok')
            try:
                kelompok = Kelompok.objects.get(nama=nama_kelompok)
                anggota_list = Anggota.objects.filter(kelompok=kelompok, is_ketua=False)
                koordinator_list = Anggota.objects.filter(kelompok=kelompok, is_ketua=True)
            except Kelompok.DoesNotExist:
                kelompok = None
                anggota_list = []
                koordinator_list = []
            if 'simpan_edit' in request.POST:
                if kelompok:  # Pastikan kelompok tidak None
                    kelompok.nama = request.POST.get('nama_kelompok', kelompok.nama)
                    kelompok.ketua = request.POST.get('ketua', kelompok.ketua)
                    kelompok.save()
                    Anggota.objects.filter(kelompok=kelompok).delete()
                    koordinator = request.POST.get('koordinator', '').strip()
                    anggota = request.POST.get('anggota', '').strip()
                    if koordinator:
                        Anggota.objects.create(nama=koordinator, kelompok=kelompok, is_ketua=True)
                    if anggota:
                        for a in anggota.splitlines():
                            a = a.strip()
                            if a:
                                Anggota.objects.create(nama=a, kelompok=kelompok)
                return redirect('panitia:daftar_kelompok')
            else:
                return render(request, 'panitia/edit_kelompok.html', {
                    'kelompok': kelompok,
                    'anggota_list': anggota_list,
                    'koordinator_list': koordinator_list,
                })
    return render(request, 'panitia/daftar_kelompok.html', {
        'kelompok_list': kelompok_list,
        'bisa_lihat': bisa_lihat,
        'bisa_edit': bisa_edit,
    })