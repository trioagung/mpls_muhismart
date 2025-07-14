from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os

# Simpan logo di media/logo.png
LOGO_PATH = os.path.join('media', 'logo.png')

@login_required
def home(request):
    logo_url = '/media/logo.png' if os.path.exists(os.path.join(settings.BASE_DIR, LOGO_PATH)) else None
    return render(request, 'main/home.html', {'logo_url': logo_url})

@login_required
def upload_logo(request):
    if request.method == 'POST' and request.FILES.get('logo'):
        logo = request.FILES['logo']
        os.makedirs(os.path.join(settings.BASE_DIR, 'media'), exist_ok=True)
        with open(os.path.join(settings.BASE_DIR, LOGO_PATH), 'wb+') as f:
            for chunk in logo.chunks():
                f.write(chunk)
        return redirect('home')
    return render(request, 'main/upload_logo.html')
