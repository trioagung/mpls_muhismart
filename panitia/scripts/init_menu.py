from panitia.models import Menu, MENU_CHOICES

def run():
    for nama, _ in MENU_CHOICES:
        Menu.objects.get_or_create(nama=nama)
    print("Menu berhasil diinisialisasi!")

# Cara pakai:
# python manage.py shell < panitia/scripts/init_menu.py
