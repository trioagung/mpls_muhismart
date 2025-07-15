from django.urls import path
from . import views
from . import views_absensi
from . import views_koordinator_ajax

app_name = 'panitia'

urlpatterns = [
    path('', views.struktur_organisasi, name='struktur_organisasi'),
    path('tugas/<str:jabatan>/', views.tugas_panitia, name='tugas_panitia'),
    path('tambah/', views.tambah_panitia, name='tambah_panitia'),
    path('hapus/<str:jabatan>/', views.hapus_panitia, name='hapus_panitia'),
    
    # AJAX endpoints untuk koordinator (hosting compatibility)
    path('ajax/tambah-koordinator/', views_koordinator_ajax.tambah_koordinator_ajax, name='tambah_koordinator_ajax'),
    path('ajax/test-database/', views_koordinator_ajax.test_database_connection, name='test_database'),
    
    # Tambahan menu IPM
    path('ipm/', views.menu_ipm, name='menu_ipm'),
    path('ipm/pelaksana/', views.panitia_pelaksana, name='panitia_pelaksana'),
    path('ipm/koordinator/', views.koordinator_kelompok, name='koordinator_kelompok'),
    path('ipm/upacara/', views.petugas_upacara, name='petugas_upacara'),
    path('ipm/tugas/<str:jabatan>/', views.tugas_pelaksana, name='tugas_pelaksana'),
    path('ipm/upacara/tugas/<str:jabatan>/', views.tugas_upacara, name='tugas_upacara'),
    path('daftar-kelompok/', views.daftar_kelompok, name='daftar_kelompok'),
    path('pengumuman/', views.pengumuman, name='pengumuman'),
    path('logistik/', views.logistik, name='logistik'),
    path('logistik/edit/<int:id>/', views.edit_logistik, name='edit_logistik'),
    path('larangan/edit/<int:id>/', views.edit_larangan, name='edit_larangan'),
    path('surat/', views.surat, name='surat'),
    path('jadwal/', views.jadwal, name='jadwal'),
    path('jadwal/edit/', views.edit_jadwal, name='edit_jadwal'),
    path('absensi/', views_absensi.absensi, name='absensi'),
    path('absensi/download/pdf/', views.download_absensi_pdf, name='download_absensi_pdf'),
    path('absensi/download/excel/', views.download_absensi_excel, name='download_absensi_excel'),
    path('keuangan/', views.keuangan, name='keuangan'),
    path('keuangan/download/excel/', views.keuangan_excel, name='keuangan_excel'),
    path('keuangan/download/pdf/', views.keuangan_pdf, name='keuangan_pdf'),
    path('keuangan/edit/<int:pk>/', views.keuangan_edit, name='keuangan_edit'),
    path('keuangan/hapus/<int:pk>/', views.keuangan_hapus, name='keuangan_hapus'),
]
