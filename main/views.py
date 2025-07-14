from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import os
import time

# Simpan logo di media/logo.png
LOGO_PATH = os.path.join('media', 'logo.png')

@login_required
def home(request):
    if os.path.exists(os.path.join(settings.BASE_DIR, LOGO_PATH)):
        # Tambahkan timestamp untuk menghindari cache browser
        timestamp = str(int(os.path.getmtime(os.path.join(settings.BASE_DIR, LOGO_PATH))))
        logo_url = f'/media/logo.png?v={timestamp}'
    else:
        logo_url = None
    return render(request, 'main/home.html', {'logo_url': logo_url})

@login_required
def upload_logo(request):
    # Cek permission - hanya staff/superuser yang bisa upload logo
    if not (request.user.is_staff or request.user.is_superuser):
        return render(request, 'main/upload_logo.html', {'error': True})
    
    if request.method == 'POST' and request.FILES.get('logo'):
        logo = request.FILES['logo']
        
        # Validasi file format
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']
        file_extension = os.path.splitext(logo.name)[1].lower()
        if file_extension not in valid_extensions:
            messages.error(request, 'Format file tidak valid. Gunakan PNG, JPG, JPEG, atau GIF.')
            return render(request, 'main/upload_logo.html')
        
        # Simpan file
        os.makedirs(os.path.join(settings.BASE_DIR, 'media'), exist_ok=True)
        logo_path = os.path.join(settings.BASE_DIR, LOGO_PATH)
        
        # Hapus logo lama jika ada
        if os.path.exists(logo_path):
            os.remove(logo_path)
        
        # Simpan logo baru
        with open(logo_path, 'wb+') as f:
            for chunk in logo.chunks():
                f.write(chunk)
                
        messages.success(request, 'Logo berhasil diupload!')
        return redirect('main:home')
    
    return render(request, 'main/upload_logo.html')
