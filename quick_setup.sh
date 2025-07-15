#!/bin/bash
# 🚀 SIMPLIFIED PYTHONANYWHERE DEPLOYMENT
# For use when you already have dependencies installed

echo "🚀 PYTHONANYWHERE QUICK SETUP"
echo "=============================="

# Setup directories
echo "📁 Creating directories..."
mkdir -p static media
chmod 755 static media

# Database setup
echo "🗃️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser
echo "👤 Creating superuser..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@mplsmuhi.com', 'admin123')
    print("✅ Superuser 'admin' created!")
else:
    print("ℹ️  Superuser 'admin' already exists")
EOF

# Create logo placeholder
echo "🎨 Creating logo placeholder..."
python << 'EOF'
try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    if not os.path.exists('media/logo.png'):
        img = Image.new('RGB', (200, 200), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text1 = "SMA MUHI 1"
        text2 = "KARTASURA"
        
        bbox1 = draw.textbbox((0, 0), text1, font=font)
        bbox2 = draw.textbbox((0, 0), text2, font=font)
        
        w1 = bbox1[2] - bbox1[0]
        w2 = bbox2[2] - bbox2[0]
        
        draw.text(((200-w1)/2, 70), text1, fill='darkblue', font=font)
        draw.text(((200-w2)/2, 100), text2, fill='darkblue', font=font)
        
        os.makedirs('media', exist_ok=True)
        img.save('media/logo.png')
        print("📸 Logo placeholder created!")
    else:
        print("📸 Logo already exists")
except ImportError:
    print("⚠️  Pillow not available, skipping logo creation")
except Exception as e:
    print(f"⚠️  Logo creation failed: {e}")
EOF

# Set permissions
echo "🔧 Setting permissions..."
chmod 755 manage.py
chmod -R 755 static media

# Test Django
echo "✅ Testing Django..."
python manage.py check

echo ""
echo "🎉 SETUP COMPLETED!"
echo "=================="
echo ""
echo "🔐 Login credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "📝 Next steps:"
echo "1. Configure your PythonAnywhere web app"
echo "2. Set source code path"
echo "3. Configure WSGI file"
echo "4. Add static/media files mapping"
echo "5. Reload your web app"
echo ""
echo "✅ MPLS MUHI SMART ready for production!"
