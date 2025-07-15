"""
Verifikasi User Admin dan Permission
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpls.settings')
django.setup()

from django.contrib.auth.models import User
from panitia.helpers import get_akses

# Cek user admin
admin_users = User.objects.filter(username='admin')
print(f"User admin yang ditemukan: {admin_users.count()}")

for user in admin_users:
    print(f"\nUser: {user.username}")
    print(f"Is superuser: {user.is_superuser}")
    print(f"Is staff: {user.is_staff}")
    print(f"Is active: {user.is_active}")
    
    # Test permission untuk menu Panitia Utama
    bisa_lihat, bisa_edit = get_akses(user, 'Panitia Utama')
    print(f"Permission Panitia Utama: lihat={bisa_lihat}, edit={bisa_edit}")
    
# Jika tidak ada user admin, buat satu
if admin_users.count() == 0:
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print(f"\n✅ User admin dibuat dengan password: admin123")
    bisa_lihat, bisa_edit = get_akses(admin_user, 'Panitia Utama')
    print(f"Permission Panitia Utama: lihat={bisa_lihat}, edit={bisa_edit}")

print("\n🎉 Verifikasi selesai!")
