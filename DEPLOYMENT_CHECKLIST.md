# 🚀 PYTHONANYWHERE DEPLOYMENT CHECKLIST
# MPLS MUHI SMART - Complete Setup Guide

## 📅 PRE-DEPLOYMENT (Done ✅)
- [x] Code tested locally
- [x] Logo display fixed (no unwanted borders)
- [x] Settings configured for hosting
- [x] Static/Media files setup
- [x] Case-insensitive database queries
- [x] Comprehensive error handling
- [x] Deployment scripts created
- [x] Repository updated on GitHub

## 🌐 PYTHONANYWHERE SETUP

### Step 1: Clone Repository
```bash
# In PythonAnywhere console:
git clone https://github.com/trioagung/mpls_muhismart.git
cd mpls_muhismart
```

### Step 2A: Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

### Step 2B: Run Quick Setup (Recommended)
```bash
chmod +x quick_setup.sh
./quick_setup.sh
```

**OR** use full deployment script:
```bash
chmod +x pythonanywhere_deploy.sh
./pythonanywhere_deploy.sh
```

### Step 3: Create Web App
1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **Python 3.10**
4. Select **Manual configuration**

### Step 4: Configure Web App
**Source code:**
```
/home/YOURUSERNAME/mpls_muhismart
```

**WSGI configuration file:**
```
/home/YOURUSERNAME/mpls_muhismart/mpls/wsgi.py
```
*Or copy content from `pythonanywhere_wsgi.py`*

### Step 5: Static Files Mapping
**URL:** `/static/`
**Directory:** `/home/YOURUSERNAME/mpls_muhismart/static`

### Step 6: Media Files Mapping  
**URL:** `/media/`
**Directory:** `/home/YOURUSERNAME/mpls_muhismart/media`

### Step 7: Reload & Test
1. Click **"Reload"** button
2. Visit your site: `https://YOURUSERNAME.pythonanywhere.com`
3. Test admin: `https://YOURUSERNAME.pythonanywhere.com/admin/`

## 🔐 DEFAULT CREDENTIALS
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@mplsmuhi.com`

## ✅ FEATURES TO TEST
- [ ] Homepage loads correctly
- [ ] Logo displays without borders
- [ ] Menu navigation works
- [ ] Admin panel accessible
- [ ] Panitia dashboard functional
- [ ] Koordinator kelompok features work
- [ ] Static files (CSS/JS) loading
- [ ] Media files (images) displaying

## 🔧 TROUBLESHOOTING

### Logo Not Displaying?
- Check media files mapping
- Verify `/media/` URL configuration
- Test: `https://YOURDOMAIN.pythonanywhere.com/media/logo.png`

### Static Files Not Loading?
- Check static files mapping
- Verify `/static/` URL configuration
- Run: `python manage.py collectstatic --noinput`

### Database Issues?
- Run: `python manage.py migrate`
- Check SQLite file permissions
- Verify database queries are case-insensitive

### Permission Errors?
- Check file permissions: `chmod -R 755 static media`
- Verify directory ownership
- Check WSGI file permissions

## 📞 SUPPORT
If you encounter issues:
1. Check PythonAnywhere error logs
2. Review console output during deployment
3. Verify all steps in this checklist
4. Test locally first to isolate issues

## 🎉 SUCCESS INDICATORS
- ✅ Website loads without errors
- ✅ Logo displays correctly (rectangular, no unwanted borders)
- ✅ Admin login works
- ✅ All menu items functional
- ✅ Static files loading (CSS styling visible)
- ✅ Database operations working (can add koordinator kelompok)

---
**🚀 MPLS MUHI SMART - Ready for Production!**
