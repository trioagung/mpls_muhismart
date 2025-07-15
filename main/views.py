from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
import os
import logging

# Setup logging
logger = logging.getLogger(__name__)

def home(request):
    """
    Homepage dengan logo handling yang robust untuk hosting environment
    """
    logo_url = None
    
    # Multiple fallback locations untuk logo
    logo_locations = [
        os.path.join(settings.MEDIA_ROOT, 'logo.png'),
        os.path.join(settings.STATIC_ROOT, 'logo.png'),
        os.path.join(settings.BASE_DIR, 'media', 'logo.png'),
        os.path.join(settings.BASE_DIR, 'static', 'logo.png'),
    ]
    
    for logo_path in logo_locations:
        if os.path.exists(logo_path) and os.path.isfile(logo_path):
            # Determine appropriate URL based on file location
            if 'media' in logo_path:
                logo_url = settings.MEDIA_URL + 'logo.png'
            else:
                logo_url = settings.STATIC_URL + 'logo.png'
            break
    
    # Debug logging for development
    if settings.DEBUG and not logo_url:
        logger.warning("Logo not found in any location:")
        for path in logo_locations:
            logger.warning(f"  - {path}: {os.path.exists(path)}")
    
    context = {
        'logo_url': logo_url,
        'debug_info': {
            'media_root': settings.MEDIA_ROOT,
            'media_url': settings.MEDIA_URL,
            'logo_found': logo_url is not None
        } if settings.DEBUG else None
    }
    return render(request, 'main/home.html', context)

def menu(request):
    """Menu utama aplikasi"""
    return render(request, 'main/menu.html')

@login_required
def upload_logo(request):
    """
    Upload logo sekolah dengan comprehensive error handling
    """
    if request.method == 'POST' and request.FILES.get('logo'):
        logo_file = request.FILES['logo']
        
        # Validate file type
        allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif']
        file_extension = os.path.splitext(logo_file.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            messages.error(request, f'File harus berformat: {", ".join(allowed_extensions)}')
            return render(request, 'main/upload_logo.html')
        
        # Validate file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if logo_file.size > max_size:
            messages.error(request, 'Ukuran file maksimal 5MB!')
            return render(request, 'main/upload_logo.html')
        
        try:
            # Ensure media directory exists
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # Save as logo.png regardless of original format
            logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
            
            # Remove existing logo if present
            if os.path.exists(logo_path):
                os.remove(logo_path)
            
            # Save new logo file
            with open(logo_path, 'wb+') as destination:
                for chunk in logo_file.chunks():
                    destination.write(chunk)
            
            # Set appropriate file permissions for PythonAnywhere
            os.chmod(logo_path, 0o644)
            
            messages.success(request, 'Logo berhasil diupload!')
            logger.info(f"Logo uploaded successfully to: {logo_path}")
            
        except PermissionError as e:
            messages.error(request, 'Error: Tidak ada permission untuk menyimpan file!')
            logger.error(f"Permission error uploading logo: {e}")
            
        except Exception as e:
            messages.error(request, f'Error upload logo: {str(e)}')
            logger.error(f"Unexpected error uploading logo: {e}")
            
        return redirect('main:home')
    
    return render(request, 'main/upload_logo.html')

@login_required
def debug_media(request):
    """
    Debug endpoint untuk troubleshooting media files
    Hanya available untuk superuser
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    debug_info = {
        'settings': {
            'MEDIA_ROOT': settings.MEDIA_ROOT,
            'MEDIA_URL': settings.MEDIA_URL,
            'STATIC_ROOT': settings.STATIC_ROOT,
            'STATIC_URL': settings.STATIC_URL,
            'DEBUG': settings.DEBUG,
        },
        'directories': {
            'media_exists': os.path.exists(settings.MEDIA_ROOT),
            'static_exists': os.path.exists(settings.STATIC_ROOT),
        },
        'files': {}
    }
    
    # Check for logo in various locations
    logo_locations = [
        ('media/logo.png', os.path.join(settings.MEDIA_ROOT, 'logo.png')),
        ('static/logo.png', os.path.join(settings.STATIC_ROOT, 'logo.png')),
    ]
    
    for name, path in logo_locations:
        debug_info['files'][name] = {
            'exists': os.path.exists(path),
            'path': path,
            'size': os.path.getsize(path) if os.path.exists(path) else None
        }
    
    # List media directory contents
    if os.path.exists(settings.MEDIA_ROOT):
        try:
            debug_info['media_contents'] = os.listdir(settings.MEDIA_ROOT)
        except:
            debug_info['media_contents'] = 'Cannot read directory'
    
    return JsonResponse(debug_info, indent=2)
