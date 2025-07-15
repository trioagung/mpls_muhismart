# ⚡ QUICK COMMANDS - COPY PASTE DI PYTHONANYWHERE CONSOLE
# Untuk update MPLS di trioagung64.pythonanywhere.com

## Command Set 1: Setup Environment
```bash
cd /home/trioagung64
source mpls-env/bin/activate
```

## Command Set 2: Navigate to Project
```bash
# Cari directory project (salah satu dari ini):
ls -la
cd mpls.muhismart/mpls_muhismart
# ATAU jika berbeda struktur:
# cd trioagung64
# cd your-project-name
```

## Command Set 3: Update Code
```bash
git reset --hard HEAD
git pull origin main
```

## Command Set 4: Update Dependencies & Database
```bash
pip install Django==5.2.4 Pillow==11.3.0
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

## Command Set 5: Create Admin & Test
```bash
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mplsmuhi.com', 'admin123')" | python manage.py shell
python manage.py check
```

## Final Step: Manual Action
- Go to: https://www.pythonanywhere.com/user/trioagung64/webapps/
- Click **"Reload"** button

## Test Results:
- Site: https://trioagung64.pythonanywhere.com
- Admin: https://trioagung64.pythonanywhere.com/admin/
- Login: admin / admin123

✅ **MPLS updated dengan semua fixes!**
