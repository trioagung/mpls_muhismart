from .models import AksesMenu

def get_akses(user, menu):
    if user.is_superuser:
        return True, True
    akses_qs = AksesMenu.objects.filter(user=user, menu=menu)
    if akses_qs.exists():
        # Ambil entry mana saja yang bisa_edit True
        bisa_lihat = any(a.bisa_lihat for a in akses_qs)
        bisa_edit = any(a.bisa_edit for a in akses_qs)
        return bisa_lihat, bisa_edit
    return False, False
