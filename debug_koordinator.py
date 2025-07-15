#!/usr/bin/env python3
"""
Debug script untuk mengecek masalah koordinator kelompok di PythonAnywhere
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/home/trioagung64/mpls.muhismart')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpls.pythonanywhere_settings')

try:
    django.setup()
    
    # Import models setelah Django setup
    from panitia.models import KoordinatorKelompok, PanitiaUtama
    from django.contrib.auth.models import User
    
    print("🔍 DEBUGGING KOORDINATOR KELOMPOK...")
    
    # 1. Check database connection
    print(f"✅ Django setup berhasil")
    
    # 2. Check if KoordinatorKelompok table exists
    try:
        count = KoordinatorKelompok.objects.count()
        print(f"✅ Model KoordinatorKelompok accessible, jumlah data: {count}")
        
        # List existing data
        for k in KoordinatorKelompok.objects.all():
            print(f"   - {k.kelompok}: {k.get_koordinator_list()}")
            
    except Exception as e:
        print(f"❌ Error accessing KoordinatorKelompok: {e}")
        print("   Kemungkinan model belum di-migrate")
    
    # 3. Check PanitiaUtama
    try:
        count = PanitiaUtama.objects.count()
        print(f"✅ Model PanitiaUtama accessible, jumlah data: {count}")
    except Exception as e:
        print(f"❌ Error accessing PanitiaUtama: {e}")
    
    # 4. Check superuser
    try:
        superusers = User.objects.filter(is_superuser=True)
        print(f"✅ Superuser count: {superusers.count()}")
        for user in superusers:
            print(f"   - {user.username}")
    except Exception as e:
        print(f"❌ Error checking users: {e}")
    
    # 5. Test create koordinator kelompok
    try:
        test_kelompok = KoordinatorKelompok.objects.create(
            kelompok="Test Debug",
            koordinator="Test User 1\nTest User 2"
        )
        print(f"✅ Test create berhasil: {test_kelompok}")
        
        # Delete test data
        test_kelompok.delete()
        print(f"✅ Test delete berhasil")
        
    except Exception as e:
        print(f"❌ Error test create/delete: {e}")
        
    print("\n📋 SOLUSI YANG DISARANKAN:")
    if KoordinatorKelompok.objects.count() == 0:
        print("1. Pastikan migration sudah dijalankan: python manage.py migrate")
        print("2. Check database permission")
    print("3. Check error logs di PythonAnywhere")
    print("4. Restart web app setelah migration")
        
except Exception as e:
    print(f"❌ Error setup Django: {e}")
    print("Pastikan path dan settings module benar")
