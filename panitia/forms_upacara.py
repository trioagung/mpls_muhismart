from django import forms

class PetugasUpacaraForm(forms.Form):
    jabatan = forms.CharField(label='Jabatan', max_length=100)
    anggota = forms.CharField(
        label='Nama Anggota (masukkan satu per baris)',
        required=True,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Masukkan satu nama anggota per baris'})
    )
    kedudukan = forms.IntegerField(label='Nilai Kedudukan (angka, 1 = paling atas)', min_value=1)
