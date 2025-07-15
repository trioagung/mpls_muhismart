from django.contrib.auth.models import User
from panitia.models import AksesMenu, MENU_CHOICES

# Ambil user admin
admin_user = User.objects.filter(username='admin').first()
if not admin_user:
    print("User admin tidak ditemukan!")
else:
    print(f"User admin ditemukan: {admin_user.username}")
    
    # Berikan akses ke semua menu
    menu_names = [choice[0] for choice in MENU_CHOICES]
    print(f"Menu yang akan diberi akses: {menu_names}")
    
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
            akses.bisa_lihat = True
            akses.bisa_edit = True
            akses.save()
            print(f"Updated: {menu_name}")
        else:
            print(f"Created: {menu_name}")
    
    print("Setup permission selesai!")
