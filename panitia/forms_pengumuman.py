from django import forms

class PengumumanForm(forms.Form):
    judul = forms.CharField(label='Judul Pengumuman', max_length=200)
    isi = forms.CharField(
        label='Isi Pengumuman',
        required=True,
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tulis isi pengumuman di sini'})
    )
