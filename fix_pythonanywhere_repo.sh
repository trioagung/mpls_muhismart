#!/bin/bash
# Script untuk fix git repository di PythonAnywhere

echo "=== Memperbaiki Git Repository di PythonAnywhere ==="

# Cek apakah folder mpls.muhismart ada
if [ -d "/home/trioagung64/mpls.muhismart" ]; then
    echo "Folder mpls.muhismart ditemukan"
    cd /home/trioagung64/mpls.muhismart
    
    # Cek apakah ini git repository
    if [ -d ".git" ]; then
        echo "Git repository ditemukan, mencoba git pull..."
        git pull origin main
    else
        echo "Bukan git repository, backup dan clone ulang..."
        cd /home/trioagung64/
        mv mpls.muhismart mpls.muhismart_backup_$(date +%Y%m%d_%H%M%S)
        git clone https://github.com/trioagung/mpls_muhismart.git mpls.muhismart
    fi
else
    echo "Folder tidak ada, clone dari GitHub..."
    cd /home/trioagung64/
    git clone https://github.com/trioagung/mpls_muhismart.git mpls.muhismart
fi

# Restart web app
echo "Restarting web app..."
touch /var/www/trioagung64_pythonanywhere_com_wsgi.py

echo "=== Selesai ==="
