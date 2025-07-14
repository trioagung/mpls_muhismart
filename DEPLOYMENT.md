# MPLS MuhiSmart - Production Deployment Guide

Aplikasi Django untuk manajemen MPLS dengan database PostgreSQL untuk penggunaan publik.

## 🚀 Recommended Hosting Platforms untuk Penggunaan Publik

### Option 1: Railway (RECOMMENDED - PostgreSQL Gratis)

**Kelebihan**: PostgreSQL gratis, auto-deploy, mudah setup
**Kapasitas**: 1GB PostgreSQL, unlimited requests

1. **Push ke GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Ready for production deployment"
   git branch -M main
   git remote add origin https://github.com/username/mpls-muhismart.git
   git push -u origin main
   ```

2. **Deploy ke Railway:**
   - Kunjungi [Railway.app](https://railway.app)
   - Login dengan GitHub → "New Project" → "Deploy from GitHub repo"
   - Pilih repository → Railway auto-detect Django
   - **Add PostgreSQL**: Click "Add Service" → "Database" → "PostgreSQL"

3. **Environment Variables di Railway:**
   ```
   DJANGO_SETTINGS_MODULE=mpls.production_settings
   SECRET_KEY=generate-strong-secret-key-here
   ```

### Option 2: Render (PostgreSQL Gratis + Robust)

**Kelebihan**: 750 jam gratis/bulan, PostgreSQL included, SSL otomatis
**Kapasitas**: 1GB PostgreSQL, auto-sleep setelah 15 menit idle

1. **Deploy ke Render:**
   - Kunjungi [Render.com](https://render.com)
   - "New" → "Web Service" → Connect GitHub repo
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn mpls.wsgi:application`

2. **Add PostgreSQL:**
   - "New" → "PostgreSQL" → Free tier
   - Copy database URL ke environment variables

### Option 3: DigitalOcean App Platform (Robust untuk Publik)

**Kelebihan**: $5/bulan, SSD storage, global CDN, auto-scaling
**Cocok untuk**: Traffic tinggi, aplikasi komersial

### Option 4: Docker + VPS (Full Control)

**Kelebihan**: Full control, custom domain, unlimited storage
**Cocok untuk**: Organisasi besar, custom requirements

```bash
# Deploy dengan Docker
docker-compose up -d

# Setup database
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py createcachetable
```

## 🗄️ Database Setup untuk Penggunaan Publik

### PostgreSQL Configuration (Auto-detect dari DATABASE_URL)
- **Production**: PostgreSQL (otomatis dari hosting)
- **Fallback**: SQLite untuk development
- **Cache**: Database cache untuk performa
- **Backup**: Otomatis di platform hosting

### Database Commands Penting:
```bash
# Migrasi database
python manage.py migrate

# Buat superuser admin
python manage.py createsuperuser

# Setup cache table untuk performa
python manage.py createcachetable

# Backup database (PostgreSQL)
pg_dump $DATABASE_URL > backup.sql
```

## 📝 Pre-deployment Checklist

- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Process definition
- ✅ `runtime.txt` - Python version
- ✅ `production_settings.py` - Production config
- ✅ `start.sh` - Start script
- ✅ Static files configuration
- ✅ Environment variables setup

## 🔧 Local Development

```bash
# Setup virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 📊 Features

- **Dashboard**: Overview sistem MPLS
- **Manajemen Siswa**: CRUD data siswa
- **Absensi**: Sistem absensi dengan permission control
- **Laporan**: Generate laporan PDF dan Excel
- **User Management**: Role-based access control

## 🔐 Default Admin

Setelah deployment, buat superuser untuk akses admin:
```bash
python manage.py createsuperuser
```

## 📱 Production URLs

- **Admin**: `/admin/`
- **Login**: `/accounts/login/`
- **Dashboard**: `/`
- **Absensi**: `/panitia/absensi/`

---
Dibuat dengan ❤️ untuk MuhiSmart
