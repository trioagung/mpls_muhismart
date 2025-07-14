@echo off
echo 🚀 MPLS MuhiSmart - Railway Auto Setup
echo ======================================

echo 📦 Installing Railway CLI...
npm install -g @railway/cli

echo 🔐 Login ke Railway...
echo Silakan login dengan akun GitHub Anda di browser yang terbuka
railway login

echo 🔗 Connecting to existing Railway project...
railway link

echo ⚙️ Setting environment variables...
railway variables set DJANGO_SETTINGS_MODULE=mpls.production_settings
railway variables set SECRET_KEY=mpls-muhismart-railway-production-trioagung-2025-secure-key
railway variables set PORT=8000
railway variables set PYTHONPATH=/app

echo 🚀 Deploying to Railway...
railway up

echo ✅ Setup completed!
echo 🌐 Your website will be available at: https://web-production-717f.up.railway.app
echo 🔧 Next: Create superuser in Railway console

pause
