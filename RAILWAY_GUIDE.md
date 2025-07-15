# 🚂 PANDUAN RAILWAY DEPLOYMENT - SUPER MUDAH!

## 🎯 Opsi 1: Setup Manual di Web (PALING MUDAH)

### Step 1: Set Environment Variables di Railway Web
1. **Buka Railway Dashboard**: https://railway.app/project/[your-project-id]
2. **Click service "Web"**
3. **Go to tab "Variables"**
4. **Tambah variables satu per satu:**

```
Variable 1:
Name: DJANGO_SETTINGS_MODULE
Value: mpls.production_settings

Variable 2:
Name: SECRET_KEY
Value: mpls-muhismart-railway-production-trioagung-2025-secure-key

Variable 3:
Name: PORT
Value: 8000
```

### Step 2: Tunggu Auto-Deploy
- Railway akan otomatis redeploy setelah environment variables ditambahkan
- Proses sekitar 3-5 menit
- Check tab "Deployments" untuk status

### Step 3: Create Admin User
1. **Setelah deployment berhasil**, go to "Deployments" tab
2. **Click deployment yang berhasil**
3. **Click "View Logs"** atau cari tombol "Connect"
4. **Run command di Railway console:**
   ```
   python manage.py createsuperuser
   ```

## 🎯 Opsi 2: Setup Otomatis dengan CLI

### Install Railway CLI
```bash
npm install -g @railway/cli
```

### Run Auto Setup
```bash
# Windows
railway_setup.bat

# Linux/Mac
chmod +x railway_setup.sh
./railway_setup.sh
```

## 🎯 Opsi 3: Manual CLI Commands

```bash
# 1. Login
railway login

# 2. Link project
railway link

# 3. Set variables
railway variables set DJANGO_SETTINGS_MODULE=mpls.production_settings
railway variables set SECRET_KEY=mpls-muhismart-railway-production-trioagung-2025-secure-key
railway variables set PORT=8000

# 4. Deploy
railway up
```

## ✅ Checklist Deployment

- [ ] PostgreSQL database sudah ditambahkan ✅ (DONE)
- [ ] Environment variables sudah diset
- [ ] Deployment berhasil (check logs)
- [ ] Website bisa diakses
- [ ] Admin user sudah dibuat
- [ ] Test login ke /admin/
- [ ] Test akses /panitia/absensi/

## 🌐 URLs Penting

- **Website**: https://web-production-717f.up.railway.app/
- **Admin**: https://web-production-717f.up.railway.app/admin/
- **Absensi**: https://web-production-717f.up.railway.app/panitia/absensi/
- **Login**: https://web-production-717f.up.railway.app/accounts/login/

## 🆘 Troubleshooting

### Problem: Deployment Failed
**Solution**: Check "Build Logs" di Railway untuk error details

### Problem: 500 Internal Server Error
**Solution**: 
1. Check environment variables sudah benar
2. Pastikan SECRET_KEY sudah diset
3. Check DATABASE_URL sudah tersedia

### Problem: Static Files Not Loading
**Solution**: Sudah handled dengan WhiteNoise, should work automatically

### Problem: Can't Access Admin
**Solution**: 
1. Create superuser dulu: `python manage.py createsuperuser`
2. Pastikan ALLOWED_HOSTS sudah include domain Railway

## 📞 Need Help?
Kalau ada error atau stuck, share screenshot error dari Railway logs!
