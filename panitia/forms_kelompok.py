from django import forms

class KelompokForm(forms.Form):
    nama_kelompok = forms.CharField(label='Nama Kelompok', max_length=100)
    koordinator = forms.CharField(
        label='Nama Koordinator Kelompok (masukkan satu per baris)',
        required=True,
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Masukkan satu nama koordinator per baris'})
    )
    ketua = forms.CharField(label='Nama Ketua Kelompok', max_length=100)
    anggota = forms.CharField(
        label='Nama Anggota Kelompok (masukkan satu per baris)',
        required=True,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Masukkan satu nama anggota per baris'})
    )
