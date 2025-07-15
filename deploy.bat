@echo off
REM Deployment script untuk Windows

echo 🚀 MPLS MUHI SMART - Auto Deployment Script
echo ============================================

REM 1. Collect static files
echo 📦 Collecting static files...
python manage.py collectstatic --noinput

REM 2. Apply migrations
echo 🗃️ Applying database migrations...
python manage.py makemigrations
python manage.py migrate

REM 3. Create superuser
echo 👤 Creating superuser...
echo from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123') | python manage.py shell

REM 4. Create media directory
echo 📁 Setting up media directory...
if not exist "media" mkdir media

echo ✅ Deployment completed successfully!
echo.
echo 📝 Ready for git push ke GitHub dan PythonAnywhere!
echo.
echo 🔐 Login credentials:
echo Username: admin
echo Password: admin123

pause
