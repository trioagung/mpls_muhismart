import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpls.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from panitia.views_panitia import struktur_organisasi

# Buat request factory
factory = RequestFactory()

# Ambil user admin
admin_user = User.objects.filter(username='admin').first()
if not admin_user:
    print("User admin tidak ditemukan!")
    exit()

# Buat request GET
request = factory.get('/panitia/struktur-organisasi/')
request.user = admin_user

# Panggil view
try:
    response = struktur_organisasi(request)
    print(f"Response status: {response.status_code}")
    
    if hasattr(response, 'context_data'):
        context = response.context_data
        print(f"Context keys: {list(context.keys()) if context else 'No context'}")
        if 'piramida' in context:
            print(f"Piramida data: {context['piramida']}")
    else:
        print("Response tidak memiliki context_data")
        
except Exception as e:
    print(f"Error calling view: {e}")
    import traceback
    traceback.print_exc()
