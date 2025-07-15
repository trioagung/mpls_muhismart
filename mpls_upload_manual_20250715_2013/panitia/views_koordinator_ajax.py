from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction, connection
from .models import KoordinatorKelompok
import json

@login_required
def tambah_koordinator_ajax(request):
    """AJAX endpoint untuk tambah koordinator kelompok"""
    if request.method == 'POST':
        try:
            kelompok = request.POST.get('kelompok', '').strip()
            koordinator_text = request.POST.get('koordinator', '').strip()
            
            print(f"[DEBUG] Received data - Kelompok: {kelompok}, Koordinator: {koordinator_text}")
            
            if not kelompok or not koordinator_text:
                return JsonResponse({
                    'success': False,
                    'error': 'Kelompok dan koordinator harus diisi!'
                })
            
            # Parse koordinator (satu per baris)
            koordinator_list = [k.strip() for k in koordinator_text.split('\n') if k.strip()]
            
            if not koordinator_list:
                return JsonResponse({
                    'success': False,
                    'error': 'Minimal harus ada satu koordinator!'
                })
            
            print(f"[DEBUG] Parsed koordinator list: {koordinator_list}")
            
            # Cek duplikasi kelompok
            if KoordinatorKelompok.objects.filter(kelompok__iexact=kelompok).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'Kelompok "{kelompok}" sudah ada!'
                })
            
            # Simpan dengan atomic transaction
            with transaction.atomic():
                print(f"[DEBUG] Creating KoordinatorKelompok...")
                koordinator_obj = KoordinatorKelompok.objects.create(
                    kelompok=kelompok,
                    koordinator=koordinator_list
                )
                print(f"[DEBUG] Created object with ID: {koordinator_obj.id}")
                
                # Verify data tersimpan
                if KoordinatorKelompok.objects.filter(id=koordinator_obj.id).exists():
                    print(f"[DEBUG] Verification successful!")
                    return JsonResponse({
                        'success': True,
                        'message': f'Koordinator kelompok "{kelompok}" berhasil ditambahkan!',
                        'data': {
                            'kelompok': koordinator_obj.kelompok,
                            'koordinator': koordinator_obj.koordinator
                        }
                    })
                else:
                    print(f"[DEBUG] Verification failed!")
                    return JsonResponse({
                        'success': False,
                        'error': 'Data tidak tersimpan dengan benar!'
                    })
                    
        except Exception as e:
            print(f"[ERROR] Exception in tambah_koordinator_ajax: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Database error: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    })

@login_required
def test_database_connection(request):
    """Test database connection dan CRUD operations"""
    if request.method == 'POST':
        try:
            print("[DEBUG] Testing database connection...")
            
            # Test basic connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            print("[DEBUG] Basic connection OK")
            
            # Count existing koordinator
            koordinator_count = KoordinatorKelompok.objects.count()
            print(f"[DEBUG] Current koordinator count: {koordinator_count}")
            
            # Test create and delete
            test_obj = None
            try:
                test_obj = KoordinatorKelompok.objects.create(
                    kelompok='TEST_KELOMPOK_DELETE_ME',
                    koordinator=['Test User']
                )
                print(f"[DEBUG] Test create successful, ID: {test_obj.id}")
                test_create_delete = True
                test_obj.delete()
                print(f"[DEBUG] Test delete successful")
            except Exception as e:
                print(f"[DEBUG] Test create/delete failed: {str(e)}")
                test_create_delete = False
                if test_obj:
                    test_obj.delete()
            
            return JsonResponse({
                'success': True,
                'koordinator_count': koordinator_count,
                'test_create_delete': test_create_delete,
                'message': 'Database connection OK'
            })
            
        except Exception as e:
            print(f"[ERROR] Database test failed: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Database connection failed: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    })
