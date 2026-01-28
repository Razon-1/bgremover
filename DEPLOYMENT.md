# Deployment Guide - Render

Complete step-by-step guide to deploy Background Remover to Render.

## 📋 Prerequisites

- GitHub account with your repository pushed
- Render account (free tier available)
- PostgreSQL database (free tier on Render)
- All code committed to GitHub

---

## 🚀 Step-by-Step Deployment Process

### STEP 1: Create Required Configuration Files

#### 1.1 Create `runtime.txt` in project root

```bash
echo "3.12.3" > runtime.txt
```

**File location**: `f:\bgremover\runtime.txt`

#### 1.2 Create `Procfile` in project root

```
web: cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 4
```

**File location**: `f:\bgremover\Procfile`

#### 1.3 Create `build.sh` in project root

```bash
#!/bin/bash

# Install dependencies
pip install -r backend/requirements.txt

# Run migrations
cd backend
python manage.py migrate
cd ..

# Collect static files
cd backend
python manage.py collectstatic --noinput
cd ..
```

**File location**: `f:\bgremover\build.sh`

**Make it executable** (in terminal):
```bash
icacls build.sh /grant Everyone:F
```

#### 1.4 Update `requirements.txt`

```bash
cd backend
```

Add these to your requirements:
```
Django==5.0
djangorestframework==3.15.1
Pillow==10.2.0
numpy==1.26.4
rembg[onnx]==2.0.57
onnxruntime==1.17.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
python-decouple==3.8
```

Save as `backend/requirements.txt`

---

### STEP 2: Update Django Settings for Production

Edit `backend/config/settings.py`:

#### 2.1 Add imports at top

```python
import os
from decouple import config

# Keep existing imports...
```

#### 2.2 Update DEBUG and ALLOWED_HOSTS

```python
# Old:
# DEBUG = True
# ALLOWED_HOSTS = []

# New:
DEBUG = config('DEBUG', default='False') == 'True'
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1').split(',')
```

#### 2.3 Add database configuration

Replace the DATABASES section:

```python
# Old DATABASES section - DELETE THIS

# New:
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```

#### 2.4 Add security settings at end of file

```python
# Security Settings for Production
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ["'self'"],
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS for production
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000').split(',')
```

#### 2.5 Update MIDDLEWARE

Add WhiteNoise middleware:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ADD THIS
    'config.cors_middleware.SimpleCORSMiddleware',
    # ... rest of middleware
]
```

#### 2.6 Update WSGI application location

In `backend/config/wsgi.py`:

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
```

---

### STEP 3: Create `.gitignore` if not exists

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# Django
*.log
local_settings.py
db.sqlite3
/media
/staticfiles

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment variables
.env
.env.local

# OS
Thumbs.db
.DS_Store
```

---

### STEP 4: Commit and Push to GitHub

```bash
cd f:\bgremover
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

---

### STEP 5: Create Database on Render

1. Go to **https://render.com**
2. Sign up or log in
3. Click **"New +"** → **"PostgreSQL"**
4. Fill in:
   - **Name**: `bgremover-db`
   - **Database**: `bgremover`
   - **User**: `bgremover`
   - **Region**: Choose closest to you
   - **Plan**: Free (0.25GB)
5. Click **"Create Database"**
6. Wait for database to create (2-3 minutes)
7. **Copy the connection string** - you'll need it later
8. Example: `postgresql://user:password@host:5432/database`

---

### STEP 6: Deploy Web Service on Render

1. Go to **https://render.com**
2. Click **"New +"** → **"Web Service"**
3. Select **"Connect a repository"**
4. Find and select **`bgremover`** repository
5. Fill in deployment settings:
   - **Name**: `bgremover-api`
   - **Environment**: `Python 3`
   - **Region**: Same as database (important!)
   - **Branch**: `main`
   - **Build Command**: `pip install -r backend/requirements.txt && cd backend && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 4`
   - **Plan**: Free (0.50 USD/month after free credits)

6. Click **"Create Web Service"**

---

### STEP 7: Configure Environment Variables

In Render dashboard for your web service:

1. Go to **Environment** tab
2. Add these variables:

```
DEBUG = False
ALLOWED_HOSTS = bgremover-api.onrender.com
DATABASE_URL = postgresql://user:password@host:5432/database
SECRET_KEY = your-secret-key-here
CORS_ALLOWED_ORIGINS = https://your-frontend-url.com,http://localhost:3000
```

**Get SECRET_KEY** (run in terminal):
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

3. Click **"Save"**

---

### STEP 8: Wait for Deployment

Render will automatically:
1. Pull your code from GitHub
2. Install dependencies
3. Run migrations
4. Collect static files
5. Start the Django server

**Check deployment logs** in Render dashboard. Wait for "Build successful" message.

---

### STEP 9: Deploy Frontend

#### Option A: Deploy Frontend on Render (Recommended)

1. In Render dashboard, click **"New +"** → **"Static Site"**
2. Connect your GitHub repository
3. Fill in:
   - **Name**: `bgremover-frontend`
   - **Branch**: `main`
   - **Build Command**: (leave empty or use `npm install` if using Node.js)
   - **Publish Directory**: `frontend`
4. Click **"Create Static Site"**
5. Go to Render dashboard for frontend
6. Copy your frontend URL (e.g., `https://bgremover-frontend.onrender.com`)

#### Option B: Deploy Frontend Separately

Use any static hosting:
- **Netlify**: https://netlify.com
- **Vercel**: https://vercel.com
- **GitHub Pages**: https://pages.github.com

---

### STEP 10: Update Frontend API URL

Edit `frontend/app.js`:

Change:
```javascript
const API_URL = 'http://127.0.0.1:8000/api';
```

To:
```javascript
const API_URL = 'https://bgremover-api.onrender.com/api';
```

Or make it dynamic:
```javascript
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://127.0.0.1:8000/api'
  : 'https://bgremover-api.onrender.com/api';
```

---

### STEP 11: Commit Frontend Changes

```bash
cd f:\bgremover
git add frontend/app.js
git commit -m "Update API URL for production"
git push origin main
```

Render will auto-redeploy frontend.

---

### STEP 12: Test Deployment

1. Open your frontend URL: `https://bgremover-frontend.onrender.com`
2. Upload an image
3. Click "Process Image"
4. Check for errors in browser console (F12)

---

## 🔧 Troubleshooting

### Issue: "502 Bad Gateway" Error

**Solution**:
1. Check Render logs (Events tab)
2. Check if migrations ran: `python manage.py migrate`
3. Restart the service: Dashboard → Manual Deploy

### Issue: Database Connection Error

**Solution**:
1. Verify DATABASE_URL is correct
2. Check PostgreSQL is running on Render
3. Ensure region matches

### Issue: "Static files not found"

**Solution**:
```bash
cd backend
python manage.py collectstatic --noinput
```

### Issue: CORS Error

**Solution**:
1. Update `CORS_ALLOWED_ORIGINS` in Render environment
2. Make sure frontend URL is exact

### Issue: Model Download Takes Too Long

**Solution**:
- Render free tier has limited resources
- First request will take 5+ minutes
- Consider upgrading to Starter plan ($7/month)
- Or pre-warm the model in your code

---

## 📊 Deployment Checklist

- [ ] `runtime.txt` created
- [ ] `Procfile` created
- [ ] `build.sh` created
- [ ] `requirements.txt` updated
- [ ] `settings.py` updated for production
- [ ] `wsgi.py` configured
- [ ] `.gitignore` created
- [ ] All changes pushed to GitHub
- [ ] PostgreSQL database created on Render
- [ ] Web service created on Render
- [ ] Environment variables set
- [ ] Deployment completed successfully
- [ ] Frontend API URL updated
- [ ] Frontend deployed
- [ ] Test upload works

---

## 📝 Important Notes

1. **First Request**: May take 5+ minutes while AI model downloads
2. **Free Tier Limits**: 
   - Web service spins down after 15 minutes of inactivity
   - First request after spin-down takes 30+ seconds
3. **Database**: 
   - Free PostgreSQL is 0.25GB (enough for metadata only)
   - Images not stored in DB (sent as base64 in response)
4. **Storage**: 
   - Render ephemeral storage - files deleted on restart
   - No persistent file storage on free tier

---

## 🔗 Useful Links

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.0/howto/deployment/
- **Gunicorn**: https://gunicorn.org/
- **PostgreSQL on Render**: https://render.com/docs/databases

---

## ✅ Success!

Once deployed:
- Backend: `https://bgremover-api.onrender.com`
- Frontend: `https://bgremover-frontend.onrender.com`
- API: `https://bgremover-api.onrender.com/api/process/`

Share your app URL with friends!

---

**Last Updated**: January 2026  
**Render Version**: Latest  
**Django**: 5.0
