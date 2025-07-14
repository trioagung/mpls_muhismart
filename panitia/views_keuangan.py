from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Keuangan
from django.http import HttpResponse
import io, xlsxwriter
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from .helpers import get_akses

@login_required
def keuangan(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Keuangan')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Keuangan'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Keuangan'})

    catatan = Keuangan.objects.all().order_by('-tanggal')
    saldo = 0
    for c in catatan:
        if c.jenis == 'masuk':
            saldo += c.jumlah
        elif c.jenis == 'keluar':
            saldo -= c.jumlah

    if request.method == 'POST':
        if 'hapus' in request.POST:
            Keuangan.objects.filter(id=request.POST['hapus']).delete()
            return redirect('panitia:keuangan')

        if 'tambah_transaksi' in request.POST:
            tanggal = request.POST.get('tanggal')
            keterangan = request.POST.get('keterangan')
            jenis = request.POST.get('jenis')
            jumlah = request.POST.get('jumlah')
            if tanggal and keterangan and jenis in ['masuk', 'keluar'] and jumlah:
                Keuangan.objects.create(
                    tanggal=tanggal,
                    keterangan=keterangan,
                    jenis=jenis,
                    jumlah=jumlah
                )
                return redirect('panitia:keuangan')

    transaksi_list = Keuangan.objects.all().order_by('-tanggal')
    pemasukan_list = Keuangan.objects.filter(jenis='masuk').order_by('-tanggal')
    pengeluaran_list = Keuangan.objects.filter(jenis='keluar').order_by('-tanggal')
    total_pemasukan = sum([t.jumlah for t in pemasukan_list])
    total_pengeluaran = sum([t.jumlah for t in pengeluaran_list])
    total_saldo = total_pemasukan - total_pengeluaran
    return render(request, 'panitia/keuangan.html', {
        'transaksi_list': transaksi_list,
        'pemasukan_list': pemasukan_list,
        'pengeluaran_list': pengeluaran_list,
        'total_pemasukan': total_pemasukan,
        'total_pengeluaran': total_pengeluaran,
        'total_saldo': total_saldo,
    })

@login_required
def keuangan_edit(request, pk):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Keuangan')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Keuangan'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Keuangan'})

    transaksi = Keuangan.objects.filter(pk=pk).first()
    if not transaksi:
        return redirect('panitia:keuangan')
    if request.method == 'POST':
        keterangan = request.POST.get('keterangan')
        jumlah = request.POST.get('jumlah')
        jenis = request.POST.get('jenis')
        if keterangan and jumlah and jenis:
            transaksi.keterangan = keterangan
            transaksi.jumlah = jumlah
            transaksi.jenis = jenis
            transaksi.save()
            return redirect('panitia:keuangan')
    return render(request, 'panitia/keuangan_edit.html', {'transaksi': transaksi})

@login_required
def keuangan_hapus(request, pk):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Keuangan')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Keuangan'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Keuangan'})

    transaksi = Keuangan.objects.filter(pk=pk).first()
    if not transaksi:
        return redirect('panitia:keuangan')
    if request.method == 'POST':
        transaksi.delete()
        return redirect('panitia:keuangan')
    return render(request, 'panitia/keuangan_hapus.html', {'transaksi': transaksi})

@login_required
def keuangan_excel(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Keuangan')
    headers = ['No', 'Keterangan', 'Jenis', 'Jumlah', 'Tanggal']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    data = Keuangan.objects.all().order_by('tanggal', 'id')
    for idx, t in enumerate(data, start=1):
        worksheet.write(idx, 0, idx)
        worksheet.write(idx, 1, t.keterangan)
        worksheet.write(idx, 2, 'Pemasukan' if t.jenis == 'masuk' else 'Pengeluaran')
        worksheet.write(idx, 3, float(t.jumlah))
        worksheet.write(idx, 4, t.tanggal.strftime('%d-%m-%Y'))
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=keuangan.xlsx'
    return response

@login_required
def keuangan_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    y = height - 40
    p.setFont('Helvetica-Bold', 16)
    p.drawCentredString(width/2, y, 'Laporan Keuangan')
    y -= 30
    p.setFont('Helvetica-Bold', 10)
    headers = ['No', 'Keterangan', 'Jenis', 'Jumlah', 'Tanggal']
    x_list = [40, 80, 300, 400, 500, 600]
    for i, header in enumerate(headers):
        p.drawString(x_list[i], y, header)
    y -= 18
    p.setFont('Helvetica', 10)
    data = Keuangan.objects.all().order_by('tanggal', 'id')
    for idx, t in enumerate(data, start=1):
        if y < 50:
            p.showPage()
            y = height - 40
            p.setFont('Helvetica-Bold', 10)
            for i, header in enumerate(headers):
                p.drawString(x_list[i], y, header)
            y -= 18
            p.setFont('Helvetica', 10)
        p.drawString(x_list[0], y, str(idx))
        p.drawString(x_list[1], y, t.keterangan)
        p.drawString(x_list[2], y, 'Pemasukan' if t.jenis == 'masuk' else 'Pengeluaran')
        p.drawString(x_list[3], y, str(t.jumlah))
        p.drawString(x_list[4], y, t.tanggal.strftime('%d-%m-%Y'))
        y -= 16
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=keuangan.pdf'
    return response
