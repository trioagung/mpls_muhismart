#!/bin/bash
# Script untuk deploy perubahan ke PythonAnywhere
# Jalankan di PythonAnywhere Bash Console

echo "=== MPLS MUHISMART DEPLOYMENT SCRIPT ==="
echo "Deploying fixes to PythonAnywhere..."

# Pindah ke direktori project
cd /home/trioagung64/mpls.muhismart

# Aktifkan virtual environment
source /home/trioagung64/.virtualenvs/mpls-env/bin/activate

echo "1. Running database migrations..."
python manage.py migrate --settings=mpls.pythonanywhere_settings

echo "2. Migrating panitia data to separate models..."
python manage.py migrate_panitia_data --settings=mpls.pythonanywhere_settings

echo "3. Collecting static files..."
python manage.py collectstatic --noinput --settings=mpls.pythonanywhere_settings

echo "4. Reloading web app..."
touch /var/www/trioagung64_pythonanywhere_com_wsgi.py

echo "=== DEPLOYMENT COMPLETED ==="
echo "Website: https://trioagung64.pythonanywhere.com"
echo ""
echo "FIXES APPLIED:"
echo "✅ Logo upload with timestamp (no more cache issues)"
echo "✅ Logo upload permission & validation"
echo "✅ Separated Panitia models (no more cross-contamination)"
echo "✅ Admin access fix for Logistik & Daftar Kelompok"
echo "✅ UI consistency - tombol kembali di dalam card"
echo ""
echo "TESTING CHECKLIST:"
echo "□ Test logo upload & display"
echo "□ Test Panitia Utama (separate from Pelaksana)"
echo "□ Test Petugas Upacara (separate from others)"
echo "□ Test admin edit access in Logistik"
echo "□ Test admin edit access in Daftar Kelompok"
echo "□ Check tugas upacara button position"
