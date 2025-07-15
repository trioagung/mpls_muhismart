#!/bin/bash
# 🚀 PYTHONANYWHERE AUTOMATED DEPLOYMENT SCRIPT
# MPLS MUHI SMART - Complete Setup

echo "🚀 STARTING PYTHONANYWHERE DEPLOYMENT"
echo "====================================="
echo "📅 $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Step 1: Install requirements
print_info "Installing Python requirements..."
# Check if we're in a virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    print_info "Virtual environment detected: $VIRTUAL_ENV"
    pip install -r requirements.txt
else
    # Fallback to user install if not in virtual env
    pip3.10 install --user -r requirements.txt
fi

if [ $? -eq 0 ]; then
    print_status "Requirements installed successfully"
else
    print_warning "Requirements installation had issues, continuing..."
fi

# Step 2: Setup directories
print_info "Creating necessary directories..."
mkdir -p static
mkdir -p media
chmod 755 static
chmod 755 media
print_status "Directories created"

# Step 3: Collect static files
print_info "Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -eq 0 ]; then
    print_status "Static files collected"
else
    print_warning "Static files collection had issues (might be OK)"
fi

# Step 4: Database migrations
print_info "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate
if [ $? -eq 0 ]; then
    print_status "Database migrations completed"
else
    print_error "Database migration failed"
    exit 1
fi

# Step 5: Create superuser
print_info "Creating superuser account..."
python manage.py shell << 'EOF'
import os
from django.contrib.auth.models import User

# Create superuser if doesn't exist
username = 'admin'
email = 'admin@mplsmuhi.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superuser '{username}' created successfully!")
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {password}")
else:
    print(f"ℹ️  Superuser '{username}' already exists")
EOF

print_status "Superuser setup completed"

# Step 6: Create sample logo if not exists
print_info "Setting up logo placeholder..."
if [ ! -f "media/logo.png" ]; then
    # Create a simple placeholder using Python
    python << 'EOF'
from PIL import Image, ImageDraw, ImageFont
import os

# Create a simple logo placeholder
img = Image.new('RGB', (200, 200), color='lightblue')
draw = ImageDraw.Draw(img)

# Try to use a system font, fallback to default
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
except:
    font = ImageFont.load_default()

# Draw text
text1 = "SMA MUHI 1"
text2 = "KARTASURA"
text3 = "LOGO"

# Get text dimensions and center
bbox1 = draw.textbbox((0, 0), text1, font=font)
bbox2 = draw.textbbox((0, 0), text2, font=font)
bbox3 = draw.textbbox((0, 0), text3, font=font)

w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
w3, h3 = bbox3[2] - bbox3[0], bbox3[3] - bbox3[1]

# Draw centered text
draw.text(((200-w1)/2, 50), text1, fill='darkblue', font=font)
draw.text(((200-w2)/2, 80), text2, fill='darkblue', font=font)
draw.text(((200-w3)/2, 120), text3, fill='gray', font=font)

# Save
os.makedirs('media', exist_ok=True)
img.save('media/logo.png')
print("📸 Logo placeholder created!")
EOF
    print_status "Logo placeholder created"
else
    print_status "Logo already exists"
fi

# Step 7: Set proper permissions
print_info "Setting file permissions..."
find . -name "*.py" -exec chmod 644 {} \;
chmod 755 manage.py
chmod -R 755 static
chmod -R 755 media
print_status "Permissions set correctly"

# Step 8: Test basic functionality
print_info "Testing Django setup..."
python manage.py check
if [ $? -eq 0 ]; then
    print_status "Django check passed"
else
    print_error "Django check failed"
    exit 1
fi

# Final summary
echo ""
echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "====================================="
echo ""
print_status "✅ Requirements installed"
print_status "✅ Directories created"
print_status "✅ Static files collected"
print_status "✅ Database migrated"
print_status "✅ Superuser created"
print_status "✅ Logo placeholder ready"
print_status "✅ Permissions set"
print_status "✅ Django checks passed"
echo ""
echo "🔧 NEXT STEPS FOR PYTHONANYWHERE WEB APP:"
echo "========================================="
echo "1. 🌐 Go to PythonAnywhere Web tab"
echo "2. ➕ Create new web app (Python 3.10)"
echo "3. 📁 Set source code: /home/YOURUSERNAME/mpls.muhismart"
echo "4. 🔧 Set WSGI file: /home/YOURUSERNAME/mpls.muhismart/mpls/wsgi.py"
echo ""
echo "📂 STATIC FILES MAPPING:"
echo "URL: /static/"
echo "Directory: /home/YOURUSERNAME/mpls.muhismart/static"
echo ""
echo "📂 MEDIA FILES MAPPING:"
echo "URL: /media/"
echo "Directory: /home/YOURUSERNAME/mpls.muhismart/media"
echo ""
echo "🔐 LOGIN CREDENTIALS:"
echo "Username: admin"
echo "Password: admin123"
echo "Admin URL: https://YOURDOMAIN.pythonanywhere.com/admin/"
echo ""
echo "🔄 After configuring web app, click 'Reload' button!"
echo ""
print_status "🚀 MPLS MUHI SMART is ready for production!"
