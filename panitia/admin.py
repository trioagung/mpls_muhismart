from django.contrib import admin
from .models import Keuangan, Kelompok, Anggota, Agenda, Absensi, AksesMenu, PanitiaPelaksana, TugasUpacara, PanitiaUtama, PetugasUpacara

admin.site.register(Keuangan)
admin.site.register(Kelompok)
admin.site.register(Anggota)
admin.site.register(Agenda)
admin.site.register(Absensi)
admin.site.register(AksesMenu)
admin.site.register(PanitiaPelaksana)
admin.site.register(PanitiaUtama)
admin.site.register(PetugasUpacara)
admin.site.register(TugasUpacara)
