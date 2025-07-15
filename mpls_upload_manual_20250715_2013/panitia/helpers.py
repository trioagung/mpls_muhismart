from .models import AksesMenu

def get_akses(user, menu):
    """
    Get user access with case-insensitive menu matching
    Fix untuk compatibility Windows → Linux hosting
    """
    if user.is_superuser:
        return True, True
    
    # Case-insensitive search untuk compatibility Windows → Linux
    akses_qs = AksesMenu.objects.filter(
        user=user, 
        menu__iexact=menu  # iexact = case-insensitive exact match
    )
    
    if akses_qs.exists():
        # Ambil entry mana saja yang bisa_edit True
        bisa_lihat = any(a.bisa_lihat for a in akses_qs)
        bisa_edit = any(a.bisa_edit for a in akses_qs)
        return bisa_lihat, bisa_edit
    return False, False
