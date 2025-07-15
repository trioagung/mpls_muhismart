#!/usr/bin/env python
"""
Script untuk memberikan akses admin ke semua menu
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpls.settings')
django.setup()

from django.contrib.auth.models import User
from panitia.models import AksesMenu, MENU_CHOICES

def setup_admin_permissions():
    """Memberikan akses penuh ke semua menu untuk user admin"""
    
    # Ambil atau buat user admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'is_staff': True,
            'is_superuser': True,
            'email': 'admin@example.com'
        }
    )
    
    if created:
        admin_user.set_password('admin123')  # Set password default
        admin_user.save()
        print(f"✅ User admin dibuat dengan password: admin123")
    else:
        print(f"✅ User admin sudah ada")
    
    # Berikan akses ke semua menu
    menu_names = [choice[0] for choice in MENU_CHOICES]
    
    for menu_name in menu_names:
        akses, created = AksesMenu.objects.get_or_create(
            user=admin_user,
            menu=menu_name,
            defaults={
                'bisa_lihat': True,
                'bisa_edit': True
            }
        )
        
        if not created:
            # Update existing permission
            akses.bisa_lihat = True
            akses.bisa_edit = True
            akses.save()
            print(f"🔄 Updated permission untuk menu: {menu_name}")
        else:
            print(f"✅ Berikan akses ke menu: {menu_name}")
    
    print(f"\n🎉 Setup permission selesai!")
    print(f"User admin sekarang bisa mengakses semua menu dengan permission penuh.")

if __name__ == '__main__':
    setup_admin_permissions()
