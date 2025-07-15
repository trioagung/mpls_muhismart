from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.shortcuts import render, redirect
from .forms import PanitiaForm
from .helpers import get_akses
from .models import PanitiaUtama

# Dummy data koordinator kelompok
KOORDINATOR_KELOMPOK = []

## Hapus STRUKTUR_ORGANISASI dummy, gunakan database PanitiaPelaksana

TUGAS_KHUSUS = {}
TUGAS_UMUM = {
    "Penanggung Jawab": [
        "Mengawasi seluruh kegiatan panitia",
        "Memberikan arahan dan keputusan akhir",
        "Menjadi penanggung jawab utama kegiatan",
        "Menyelesaikan masalah strategis",
        "Menjadi penghubung dengan pihak eksternal"
    ],
    "Ketua Panitia": [
        "Mengkoordinasi seluruh panitia",
        "Membuat jadwal kegiatan",
        "Memimpin rapat panitia",
        "Mengawasi pelaksanaan tugas",
        "Menyusun laporan kegiatan"
    ],
    "Sekretaris": [
        "Mencatat hasil rapat",
        "Mengelola administrasi",
        "Membuat surat-menyurat",
        "Menyimpan dokumen penting",
        "Membantu ketua dalam administrasi"
    ],
    "Bendahara": [
        "Mengelola keuangan",
        "Membuat laporan keuangan",
        "Mencatat pemasukan dan pengeluaran",
        "Menyimpan bukti transaksi",
        "Membantu ketua dalam hal keuangan"
    ],
    "Pelaksana": [
        "Melaksanakan tugas teknis",
        "Membantu kelancaran acara",
        "Menyiapkan perlengkapan",
        "Mengatur peserta",
        "Membantu panitia lain"
    ],
}

def struktur_piramida(struktur):
    tree = {}
    lookup = {item['nama']: {**item, 'children': []} for item in struktur}
    for item in lookup.values():
        if item.get('parent') and item['parent'] in lookup:
            lookup[item['parent']]['children'].append(item)
        else:
            tree[item['nama']] = item
    return tree

@login_required
def struktur_organisasi(request):
    from .models import KoordinatorKelompok
    
    bisa_lihat, bisa_edit = get_akses(request.user, 'Panitia Utama')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Panitia Utama'})
    
    struktur_sorted = list(PanitiaUtama.objects.all().order_by('kedudukan', 'jabatan'))
    piramida = defaultdict(list)
    for item in struktur_sorted:
        piramida[item.kedudukan].append({
            'nama': item.jabatan,
            'kedudukan': item.kedudukan,
            'anggota': item.anggota_list(),
            'tugas': '',
        })
    
    # Ambil data koordinator kelompok dari database
    koordinator_list = KoordinatorKelompok.objects.all().order_by('kelompok')
    koordinator_data = []
    for k in koordinator_list:
        koordinator_data.append({
            "id": k.id,
            "kelompok": k.kelompok, 
            "koordinator": k.get_koordinator_list()
        })
    
    tree = struktur_piramida([{'nama': p.jabatan, 'kedudukan': p.kedudukan, 'parent': None, 'tugas': ''} for p in struktur_sorted])
    
    # Variable untuk menyimpan pesan error/success
    koordinator_message = None
    koordinator_error = None
    
    # Handle POST requests untuk koordinator kelompok
    if request.method == "POST" and bisa_edit:
        # Log semua POST data untuk debugging
        print(f"=== DEBUG POST DATA ===")
        for key, value in request.POST.items():
            print(f"POST[{key}] = {value}")
        print(f"=== END POST DATA ===")
        
        if 'tambah_koordinator' in request.POST:
            kelompok = request.POST.get('kelompok', '').strip()
            koordinator_input = request.POST.get('koordinator', '').strip()
            is_ajax_fallback = request.POST.get('ajax_fallback') == '1'
            
            print(f"DEBUG: Form values - Kelompok: '{kelompok}', Koordinator: '{koordinator_input}'")
            print(f"DEBUG: AJAX fallback mode: {is_ajax_fallback}")
            print(f"DEBUG: Validation - kelompok empty: {not kelompok}, koordinator empty: {not koordinator_input}")
            
            if kelompok and koordinator_input:
                try:
                    # Debug: Print database state sebelum create
                    count_before = KoordinatorKelompok.objects.count()
                    print(f"DEBUG: Database count before create: {count_before}")
                    
                    # Check if already exists
                    if KoordinatorKelompok.objects.filter(kelompok=kelompok).exists():
                        koordinator_error = f"Kelompok '{kelompok}' sudah ada"
                        print(f"DEBUG: Kelompok already exists: {kelompok}")
                    else:
                        # Use different approaches based on environment
                        if is_ajax_fallback:
                            # Simple approach for fallback
                            new_koordinator = KoordinatorKelompok(
                                kelompok=kelompok,
                                koordinator=koordinator_input
                            )
                            new_koordinator.save()
                            print(f"DEBUG: Fallback save completed")
                        else:
                            # Use atomic transaction untuk memastikan data benar-benar tersimpan
                            from django.db import transaction
                            with transaction.atomic():
                                new_koordinator = KoordinatorKelompok.objects.create(
                                    kelompok=kelompok,
                                    koordinator=koordinator_input
                                )
                                print(f"DEBUG: Atomic create completed with PK: {new_koordinator.pk}")
                        
                        # Check database count setelah create
                        count_after = KoordinatorKelompok.objects.count()
                        print(f"DEBUG: Database count after create: {count_after}")
                        
                        # Verify data tersimpan dengan query
                        verify = KoordinatorKelompok.objects.filter(kelompok=kelompok).exists()
                        print(f"DEBUG: Verification check - kelompok '{kelompok}' exists: {verify}")
                        
                        if verify:
                            print(f"DEBUG: SUCCESS - Data berhasil tersimpan ke database")
                            koordinator_message = f"Berhasil menambah koordinator kelompok: {kelompok}"
                        else:
                            print(f"DEBUG: ERROR - Data tidak ditemukan setelah create")
                            koordinator_error = "Data tidak berhasil disimpan ke database"
                    
                    print(f"DEBUG: Setting success message: {koordinator_message}")
                    return redirect('panitia:struktur_organisasi')
                    
                except Exception as e:
                    print(f"ERROR: Failed to create KoordinatorKelompok: {str(e)}")
                    print(f"ERROR: Exception type: {type(e)}")
                    import traceback
                    print(f"ERROR: Traceback: {traceback.format_exc()}")
                    koordinator_error = f"Error menambah koordinator: {str(e)}"
            else:
                koordinator_error = "Kelompok dan koordinator harus diisi"
                print(f"DEBUG: Validation failed - empty fields")
                
        elif 'hapus_koordinator' in request.POST:
            try:
                idx = int(request.POST.get('hapus_koordinator'))
                if 0 <= idx < len(koordinator_data):
                    koordinator_id = koordinator_data[idx]['id']
                    deleted_count, _ = KoordinatorKelompok.objects.filter(id=koordinator_id).delete()
                    print(f"DEBUG: Deleted {deleted_count} KoordinatorKelompok records")
                    koordinator_message = "Berhasil menghapus koordinator kelompok"
                    return redirect('panitia:struktur_organisasi')
                else:
                    koordinator_error = "Data koordinator tidak ditemukan"
            except Exception as e:
                print(f"ERROR: Failed to delete KoordinatorKelompok: {str(e)}")
                koordinator_error = f"Error menghapus koordinator: {str(e)}"
                
        elif 'edit_koordinator' in request.POST:
            # Check if this is just requesting edit form (no actual data to save)
            if not ('kelompok_edit' in request.POST and 'koordinator_edit' in request.POST):
                # This is just requesting the edit form, set edit_idx and don't redirect
                edit_idx = request.POST.get('edit_koordinator')
                print(f"DEBUG: Requesting edit form for koordinator idx: {edit_idx}")
            else:
                # This is actual form submission with data
                try:
                    idx = int(request.POST.get('edit_koordinator'))
                    if 0 <= idx < len(koordinator_data):
                        koordinator_id = koordinator_data[idx]['id']
                        kelompok = request.POST.get('kelompok_edit', '').strip()
                        koordinator_input = request.POST.get('koordinator_edit', '').strip()
                        
                        print(f"DEBUG: Editing koordinator - idx: {idx}, id: {koordinator_id}, kelompok: {kelompok}")
                        
                        if kelompok and koordinator_input:
                            # Use atomic transaction
                            from django.db import transaction
                            with transaction.atomic():
                                k = KoordinatorKelompok.objects.get(id=koordinator_id)
                                k.kelompok = kelompok
                                k.koordinator = koordinator_input
                                k.save()
                                
                                # Verify update
                                updated_k = KoordinatorKelompok.objects.get(id=koordinator_id)
                                print(f"DEBUG: Verified update - kelompok: {updated_k.kelompok}")
                            
                            print(f"DEBUG: Successfully updated KoordinatorKelompok - {kelompok}")
                            koordinator_message = f"Berhasil mengupdate koordinator kelompok: {kelompok}"
                            
                            return redirect('panitia:struktur_organisasi')
                        else:
                            koordinator_error = "Kelompok dan koordinator harus diisi"
                    else:
                        koordinator_error = "Data koordinator tidak ditemukan"
                except Exception as e:
                    print(f"ERROR: Failed to update KoordinatorKelompok: {str(e)}")
                    import traceback
                    print(f"ERROR: Traceback: {traceback.format_exc()}")
                    koordinator_error = f"Error mengupdate koordinator: {str(e)}"
        
        # Handle POST untuk panitia utama            
        elif 'tambah_panitia' in request.POST:
            jabatan = request.POST.get('jabatan', '').strip()
            anggota = request.POST.get('anggota', '').strip()
            kedudukan = request.POST.get('kedudukan', '99').strip()
            try:
                kedudukan_int = int(kedudukan)
            except (ValueError, TypeError):
                kedudukan_int = 99
            if jabatan and anggota:
                PanitiaUtama.objects.create(jabatan=jabatan, anggota=anggota, kedudukan=kedudukan_int)
                return redirect('panitia:struktur_organisasi')
        elif 'hapus_panitia' in request.POST:
            jabatan = request.POST.get('hapus_panitia', '').strip()
            PanitiaUtama.objects.filter(jabatan=jabatan).delete()
            return redirect('panitia:struktur_organisasi')
        elif 'edit_panitia' in request.POST:
            jabatan = request.POST.get('edit_panitia', '').strip()
            anggota = request.POST.get('anggota_edit', '').strip()
            kedudukan = request.POST.get('kedudukan_edit', '99').strip()
            try:
                kedudukan_int = int(kedudukan)
            except (ValueError, TypeError):
                kedudukan_int = 99
            obj = PanitiaUtama.objects.filter(jabatan=jabatan).first()
            if obj and anggota:
                obj.anggota = anggota
                obj.kedudukan = kedudukan_int
                obj.save()
                return redirect('panitia:struktur_organisasi')
    
    edit_idx = None
    if request.method == "POST":
        # Handle edit request for panitia utama
        if 'edit_panitia' in request.POST and not ('anggota_edit' in request.POST or 'kedudukan_edit' in request.POST):
            edit_idx = request.POST.get('edit_panitia')
        # Handle edit request for koordinator kelompok  
        elif 'edit_koordinator' in request.POST and not ('kelompok_edit' in request.POST and 'koordinator_edit' in request.POST):
            edit_idx = request.POST.get('edit_koordinator')
            print(f"DEBUG: Setting edit_idx for koordinator: {edit_idx}")
    
    return render(request, 'panitia/struktur_organisasi.html', {
        "struktur": struktur_sorted,
        "piramida": dict(piramida),
        "struktur_piramida": tree,
        "koordinator_kelompok": koordinator_data,
        "edit_idx": edit_idx,
        "bisa_lihat": bisa_lihat,
        "bisa_edit": bisa_edit,
        "koordinator_message": koordinator_message,
        "koordinator_error": koordinator_error,
    })

@login_required
def tugas_panitia(request, jabatan):
    # Analisis jabatan secara fleksibel (case-insensitive, substring match)
    jabatan_lower = jabatan.lower()
    tugas_umum = None
    best_match = None
    best_score = 0
    for key in TUGAS_UMUM:
        key_lower = key.lower()
        # Skor kemiripan: jumlah kata yang cocok
        score = sum(1 for word in jabatan_lower.split() if word in key_lower)
        if key_lower in jabatan_lower or jabatan_lower in key_lower:
            score += 2
        if score > best_score:
            best_score = score
            best_match = key
    if best_match:
        tugas_umum = TUGAS_UMUM[best_match][:5]
    else:
        tugas_umum = ["Tidak ada tugas umum untuk jabatan ini."]
    tugas_khusus = TUGAS_KHUSUS.get(jabatan, [])
    if request.method == "POST":
        if 'tambah_tugas' in request.POST:
            tugas_baru = request.POST.get('tugas_khusus', '').strip()
            if tugas_baru:
                TUGAS_KHUSUS.setdefault(jabatan, []).append({"tugas": tugas_baru, "selesai": False})
        elif 'toggle_selesai' in request.POST:
            idx = int(request.POST.get('toggle_selesai'))
            if 0 <= idx < len(tugas_khusus):
                tugas_khusus[idx]["selesai"] = not tugas_khusus[idx]["selesai"]
        elif 'hapus_tugas' in request.POST:
            idx = int(request.POST.get('hapus_tugas'))
            if 0 <= idx < len(tugas_khusus):
                tugas_khusus.pop(idx)
        return redirect('panitia:tugas_panitia', jabatan=jabatan)
    return render(request, 'panitia/tugas_panitia.html', {
        "jabatan": jabatan,
        "tugas_umum": tugas_umum,
        "tugas_khusus": tugas_khusus,
    })

@login_required
def tambah_panitia(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Panitia Utama')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Panitia Utama'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Panitia Utama'})
        
    if request.method == 'POST':
        # Handle form langsung dari template
        jabatan = request.POST.get('jabatan', '').strip()
        anggota = request.POST.get('anggota', '').strip()
        kedudukan = request.POST.get('kedudukan', '99').strip()
        
        if jabatan and anggota:
            try:
                kedudukan_int = int(kedudukan)
            except (ValueError, TypeError):
                kedudukan_int = 99
            
            PanitiaUtama.objects.create(
                jabatan=jabatan, 
                anggota=anggota, 
                kedudukan=kedudukan_int
            )
            return redirect('panitia:struktur_organisasi')
    
    return render(request, 'panitia/tambah_panitia.html', {
        'bisa_lihat': bisa_lihat,
        'bisa_edit': bisa_edit
    })

@login_required
def hapus_panitia(request, jabatan):
    panitia = PanitiaUtama.objects.filter(jabatan=jabatan).first()
    if not panitia:
        return redirect('panitia:struktur_organisasi')
    if request.method == 'POST':
        panitia.delete()
        return redirect('panitia:struktur_organisasi')
    return render(request, 'panitia/hapus_panitia.html', {'panitia': panitia})

@login_required
def panitia_utama(request):
    bisa_lihat, bisa_edit = get_akses(request.user, 'Panitia Utama')
    if not bisa_lihat:
        return render(request, 'panitia/no_access.html', {'menu': 'Panitia Utama'})
    if request.method == 'POST' and not bisa_edit:
        return render(request, 'panitia/no_access.html', {'menu': 'Panitia Utama'})
    return redirect('panitia:struktur_organisasi')
