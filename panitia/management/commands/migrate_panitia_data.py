from django.core.management.base import BaseCommand
from panitia.models import PanitiaPelaksana, PanitiaUtama, PetugasUpacara

class Command(BaseCommand):
    help = 'Memindahkan data PanitiaPelaksana ke model yang tepat berdasarkan jenis jabatan'

    def handle(self, *args, **options):
        # Keywords untuk menentukan kategori
        upacara_keywords = ['upacara', 'pemimpin upacara', 'petugas upacara', 'pembawa bendera', 'pengibar bendera']
        utama_keywords = ['ketua', 'sekretaris', 'bendahara', 'penangung jawab', 'penanggung jawab', 'koordinator utama']
        
        moved_to_utama = 0
        moved_to_upacara = 0
        kept_in_pelaksana = 0
        
        for item in PanitiaPelaksana.objects.all():
            jabatan_lower = item.jabatan.lower()
            
            # Cek apakah jabatan untuk upacara
            if any(keyword in jabatan_lower for keyword in upacara_keywords):
                PetugasUpacara.objects.create(
                    jabatan=item.jabatan,
                    anggota=item.anggota,
                    kedudukan=item.kedudukan
                )
                item.delete()
                moved_to_upacara += 1
                self.stdout.write(f"Moved to PetugasUpacara: {item.jabatan}")
                
            # Cek apakah jabatan untuk panitia utama
            elif any(keyword in jabatan_lower for keyword in utama_keywords):
                PanitiaUtama.objects.create(
                    jabatan=item.jabatan,
                    anggota=item.anggota,
                    kedudukan=item.kedudukan
                )
                item.delete()
                moved_to_utama += 1
                self.stdout.write(f"Moved to PanitiaUtama: {item.jabatan}")
                
            # Sisanya tetap di PanitiaPelaksana
            else:
                kept_in_pelaksana += 1
                self.stdout.write(f"Kept in PanitiaPelaksana: {item.jabatan}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Data migration completed!\n"
                f"Moved to PanitiaUtama: {moved_to_utama}\n"
                f"Moved to PetugasUpacara: {moved_to_upacara}\n"
                f"Kept in PanitiaPelaksana: {kept_in_pelaksana}"
            )
        )
