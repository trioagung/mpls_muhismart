#!/bin/bash
# 🚀 PYTHONANYWHERE MANUAL DEPLOYMENT - NO CONFLICTS
# Run this in your PythonAnywhere console

echo "🚀 PYTHONANYWHERE MANUAL SETUP"
echo "=============================="
echo "📅 $(date)"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Resolve git conflicts first
print_info "Resolving git conflicts..."
git reset --hard HEAD
git pull origin main

# Install dependencies (without --user flag)
print_info "Installing dependencies..."
pip install Django==5.2.4 Pillow==11.3.0

# Setup directories
print_info "Creating directories..."
mkdir -p static media
chmod 755 static media

# Database setup
print_info "Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
print_info "Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mplsmuhi.com', 'admin123')" | python manage.py shell

# Collect static files
print_info "Collecting static files..."
python manage.py collectstatic --noinput

# Create simple logo
print_info "Creating logo placeholder..."
python -c "
try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    img = Image.new('RGB', (200, 200), color='lightblue')
    draw = ImageDraw.Draw(img)
    draw.text((30, 80), 'SMA MUHI 1', fill='darkblue')
    draw.text((50, 110), 'KARTASURA', fill='darkblue')
    os.makedirs('media', exist_ok=True)
    img.save('media/logo.png')
    print('Logo created!')
except Exception as e:
    print(f'Logo creation failed: {e}')
"

# Set permissions
print_info "Setting permissions..."
chmod 755 manage.py
find . -name '*.py' -exec chmod 644 {} \;

# Test Django
print_info "Testing Django..."
python manage.py check

echo ""
print_status "🎉 DEPLOYMENT COMPLETED!"
echo ""
echo "🔐 LOGIN CREDENTIALS:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "📝 NEXT STEPS:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Create new web app (Python 3.10)"
echo "3. Set source code: /home/YOURUSERNAME/mpls.muhismart/mpls_muhismart"
echo "4. Set WSGI: /home/YOURUSERNAME/mpls.muhismart/mpls_muhismart/mpls/wsgi.py"
echo "5. Static files: URL=/static/ Dir=/home/YOURUSERNAME/mpls.muhismart/mpls_muhismart/static"
echo "6. Media files: URL=/media/ Dir=/home/YOURUSERNAME/mpls.muhismart/mpls_muhismart/media"
echo "7. Reload web app"
echo ""
print_status "✅ MPLS MUHI SMART ready for production!"
