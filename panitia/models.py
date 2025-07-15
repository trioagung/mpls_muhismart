from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Pengumuman(models.Model):
    judul = models.CharField(max_length=200)
    isi = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

class Kelompok(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    ketua = models.CharField(max_length=100)
    # anggota dan koordinator bisa dibuat relasi jika ingin lebih kompleks

    def __str__(self):
        return self.nama

class Agenda(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    urutan = models.PositiveIntegerField(default=0)  # urutan agenda
    
    class Meta:
        ordering = ['urutan']
    
    def __str__(self):
        return self.nama

class Anggota(models.Model):
    nama = models.CharField(max_length=100)
    kelompok = models.ForeignKey(Kelompok, on_delete=models.CASCADE, related_name='anggota')
    is_ketua = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nama} ({self.kelompok.nama})"

class Absensi(models.Model):
    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    hadir = models.BooleanField(default=False)

    class Meta:
        unique_together = ('anggota', 'agenda')

    def __str__(self):
        return f"{self.anggota.nama} - {self.agenda.nama}: {'Hadir' if self.hadir else 'Tidak'}"

class Keuangan(models.Model):
    JENIS_CHOICES = (
        ('masuk', 'Pemasukan'),
        ('keluar', 'Pengeluaran'),
    )
    keterangan = models.CharField(max_length=255)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    jenis = models.CharField(max_length=10, choices=JENIS_CHOICES)
    tanggal = models.DateField(default=timezone.now)


    def __str__(self):
        return f"{self.keterangan} - {self.jenis} - {self.jumlah}"



class BarangLogistik(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    jumlah = models.PositiveIntegerField(default=1)
    waktu = models.DateTimeField(auto_now_add=True)
    jenis = models.CharField(max_length=20, choices=(('pribadi', 'Pribadi'), ('kelompok', 'Kelompok')))

    def __str__(self):
        return f"{self.nama} x{self.jumlah}"

class LaranganBarang(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

MENU_CHOICES = [
    ("Panitia Utama", "Panitia Utama"),
    ("Panitia IPM", "Panitia IPM"),
    ("Koordinator Kelompok", "Koordinator Kelompok"),
    ("Petugas Upacara", "Petugas Upacara"),
    ("Panitia Pelaksana", "Panitia Pelaksana"),
    ("Daftar Kelompok", "Daftar Kelompok"),
    ("Pengumuman", "Pengumuman"),
    ("Logistik", "Logistik"),
    ("Surat-surat", "Surat-surat"),
    ("Jadwal Kegiatan", "Jadwal Kegiatan"),
    ("Absensi", "Absensi"),
    ("Keuangan", "Keuangan"),
]

class Menu(models.Model):
    nama = models.CharField(max_length=50, choices=MENU_CHOICES, unique=True)
    def __str__(self):
        return self.nama

class AksesMenu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.CharField(max_length=50, choices=MENU_CHOICES)
    bisa_lihat = models.BooleanField(default=False)
    bisa_edit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.menu}"

class PanitiaPelaksana(models.Model):
    jabatan = models.CharField(max_length=100)
    anggota = models.TextField(help_text="Masukkan satu nama per baris")
    kedudukan = models.PositiveIntegerField(default=99)

    def anggota_list(self):
        return [a.strip() for a in self.anggota.splitlines() if a.strip()]

    def __str__(self):
        return f"Pelaksana - {self.jabatan} (kedudukan: {self.kedudukan})"

class PanitiaUtama(models.Model):
    jabatan = models.CharField(max_length=100)
    anggota = models.TextField(help_text="Masukkan satu nama per baris")
    kedudukan = models.PositiveIntegerField(default=99)

    def anggota_list(self):
        return [a.strip() for a in self.anggota.splitlines() if a.strip()]

    def __str__(self):
        return f"Utama - {self.jabatan} (kedudukan: {self.kedudukan})"

class PetugasUpacara(models.Model):
    jabatan = models.CharField(max_length=100)
    anggota = models.TextField(help_text="Masukkan satu nama per baris")
    kedudukan = models.PositiveIntegerField(default=99)

    def anggota_list(self):
        return [a.strip() for a in self.anggota.splitlines() if a.strip()]

    def __str__(self):
        return f"Upacara - {self.jabatan} (kedudukan: {self.kedudukan})"

class TugasUpacara(models.Model):
    jabatan = models.CharField(max_length=100)
    tugas = models.TextField()
    selesai = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.jabatan}: {self.tugas[:30]}{'...' if len(self.tugas) > 30 else ''}"

class KoordinatorKelompok(models.Model):
    kelompok = models.CharField(max_length=100)
    koordinator = models.TextField()  # Simpan nama koordinator, dipisah newline
    waktu = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.kelompok}"
    
    def get_koordinator_list(self):
        """Return list koordinator dari field koordinator yang dipisah newline"""
        return [k.strip() for k in self.koordinator.splitlines() if k.strip()]
    
    class Meta:
        ordering = ['kelompok']
        verbose_name = "Koordinator Kelompok"
        verbose_name_plural = "Koordinator Kelompok"

class Jadwal(models.Model):
    HARI_CHOICES = (
        (1, 'Hari 1'),
        (2, 'Hari 2'),
    )
    hari = models.IntegerField(choices=HARI_CHOICES)
    waktu = models.CharField(max_length=50)
    plan_a = models.TextField()
    plan_b = models.TextField()
    urutan = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['hari', 'urutan']
        unique_together = ['hari', 'urutan']
    
    def __str__(self):
        return f"Hari {self.hari} - {self.waktu}"
