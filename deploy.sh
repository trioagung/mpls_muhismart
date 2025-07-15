#!/bin/bash
# Deployment script untuk PythonAnywhere

echo "🚀 MPLS MUHI SMART - Auto Deployment Script"
echo "============================================"

# 1. Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# 2. Apply migrations
echo "🗃️ Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# 3. Create superuser if doesn't exist
echo "👤 Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created with password 'admin123'")
else:
    print("Superuser 'admin' already exists")
EOF

# 4. Create media directory and set permissions
echo "📁 Setting up media directory..."
mkdir -p media
chmod 755 media

# 5. Create dummy logo if doesn't exist
if [ ! -f "media/logo.png" ]; then
    echo "🎨 Creating placeholder logo..."
    # Create a simple placeholder image
    convert -size 200x200 xc:lightblue -font Arial -pointsize 24 -fill black -gravity center -annotate +0+0 "LOGO\nSEKOLAH" media/logo.png 2>/dev/null || echo "ImageMagick not available, logo placeholder not created"
fi

echo "✅ Deployment completed successfully!"
echo ""
echo "📝 Next steps for PythonAnywhere:"
echo "1. Upload semua file ke hosting"
echo "2. Set Web app source code ke: /home/yourusername/mpls.muhismart"
echo "3. Set WSGI configuration file ke: /home/yourusername/mpls.muhismart/mpls/wsgi.py"
echo "4. Add static files mapping: URL=/static/ Directory=/home/yourusername/mpls.muhismart/static"
echo "5. Add media files mapping: URL=/media/ Directory=/home/yourusername/mpls.muhismart/media"
echo "6. Reload web app"
echo ""
echo "🔐 Login credentials:"
echo "Username: admin"
echo "Password: admin123"
