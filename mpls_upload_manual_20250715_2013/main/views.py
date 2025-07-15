from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import os

def home(request):
    """Homepage dengan logo yang compatible untuk hosting"""
    # Use Django MEDIA_URL untuk compatibility dengan hosting environment
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
    
    if os.path.exists(logo_path):
        # Use MEDIA_URL yang sudah dikonfigurasi di settings
        logo_url = settings.MEDIA_URL + 'logo.png'
    else:
        logo_url = None
    
    context = {
        'logo_url': logo_url
    }
    return render(request, 'main/home.html', context)

@login_required
def upload_logo(request):
    """Upload logo sekolah"""
    if request.method == 'POST' and request.FILES.get('logo'):
        logo_file = request.FILES['logo']
        
        # Simpan ke media/logo.png
        logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
        
        # Pastikan direktori media ada
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # Simpan file
        with open(logo_path, 'wb+') as destination:
            for chunk in logo_file.chunks():
                destination.write(chunk)
        
        messages.success(request, 'Logo berhasil diupload!')
        return redirect('main:home')
    
    return render(request, 'main/upload_logo.html')
