# Deploy to Render Guide

Complete step-by-step guide to deploy your Background Remover app to Render.

## 📋 Prerequisites

- GitHub account with your repository pushed
- Render account (free tier available)
- PostgreSQL database (provided by Render)

## 🚀 Step 1: Push to GitHub

```bash
cd f:\bgremover
git add .
git commit -m "Add Render deployment files"
git push origin main
```

## 🚀 Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (recommended for easy integration)
3. Authorize Render to access your GitHub repositories

## 🚀 Step 3: Deploy Backend API

### Create Web Service:

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Select your `bgremover` repository
4. Fill in these details:
   - **Name**: `bgremover-api`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r backend/requirements.txt && cd backend && python manage.py collectstatic --no-input && python manage.py migrate`
   - **Start Command**: `gunicorn config.wsgi:application --chdir backend --bind 0.0.0.0:$PORT`
   - **Plan**: Free (or paid for better performance)

### Add Environment Variables:

Click **"Advanced"** and add these environment variables:

```
DEBUG=False
SECRET_KEY=your-super-secret-key-here-generate-a-random-string
ALLOWED_HOSTS=bgremover-api.onrender.com,your-frontend-domain.onrender.com
DATABASE_URL=postgresql://user:password@host/database
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.onrender.com
ENVIRONMENT=production
```

**Note**: After creating the service, Render will provide the PostgreSQL DATABASE_URL automatically.

4. Click **"Create Web Service"**
5. Wait for deployment (2-5 minutes)

## 🚀 Step 4: Generate Secret Key

Before deploying, generate a secure SECRET_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy this value and paste it in Render environment variables.

## 🚀 Step 5: Deploy Frontend

### Create Static Site:

1. Go to Render dashboard
2. Click **"New +"** → **"Static Site"**
3. Select your `bgremover` repository
4. Fill in:
   - **Name**: `bgremover-frontend`
   - **Branch**: `main`
   - **Build Command**: `echo "No build needed"`
   - **Publish Directory**: `frontend`

5. Click **"Create Static Site"**

## 🚀 Step 6: Update Frontend API URL

After deploying backend, update your frontend to use the Render API URL:

**In `frontend/app.js`**, change:
```javascript
// OLD:
const response = await fetch('http://127.0.0.1:8000/api/process/', {

// NEW:
const response = await fetch('https://bgremover-api.onrender.com/api/process/', {
```

Replace `bgremover-api` with your actual Render service name.

Then push this change:
```bash
git add frontend/app.js
git commit -m "Update API endpoint for Render deployment"
git push origin main
```

## 🚀 Step 7: Set Up CORS

Your backend CORS middleware should already handle this, but verify:

In `backend/config/settings.py`, the frontend domain is in `CORS_ALLOWED_ORIGINS`:

```python
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000'
).split(',')
```

And in Render environment variables:
```
CORS_ALLOWED_ORIGINS=https://bgremover-frontend.onrender.com
```

## ✅ Testing

1. Navigate to your frontend URL: `https://bgremover-frontend.onrender.com`
2. Try uploading an image
3. Check browser console (F12) for any errors
4. Check Render logs for backend errors

**View Logs:**
- Backend: Dashboard → bgremover-api → Logs
- Frontend: Dashboard → bgremover-frontend → Logs

## 🐛 Troubleshooting

### "Failed to fetch" on upload
- Check CORS_ALLOWED_ORIGINS environment variable
- Verify backend service name is correct in frontend app.js
- Check backend logs for errors

### Database migrations not running
- Go to backend service → Shell
- Run: `python manage.py migrate`

### Models not found
- Ensure `INSTALLED_APPS` in settings.py includes `'apps.images'`
- Check migrations folder exists and has proper files

### Out of memory on free tier
- Large AI model (rembg) uses significant memory
- Consider upgrading to paid tier
- Or implement image preprocessing to reduce size

### First request times out
- Free tier cold starts can take 30-50 seconds
- This is normal; subsequent requests are faster
- Consider upgrading to paid tier for better performance

## 📊 Performance Tips

1. **Model Download**: On first request, AI model downloads (~300MB) - can take 5+ minutes
2. **Image Size**: Automatically downsampled to 1024px for faster processing
3. **Cold Starts**: Free tier goes to sleep after inactivity (takes 30s to wake up)
4. **Memory**: Upgrade to paid tier if you need faster processing

## 💾 Backup Database

Render provides free PostgreSQL. To export/backup:

1. Dashboard → select database service
2. Look for export/backup options
3. Or use command line:
   ```bash
   pg_dump $DATABASE_URL > backup.sql
   ```

## 🔐 Security Checklist

- [ ] Change SECRET_KEY to a random string
- [ ] Set DEBUG=False
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] Use HTTPS only (Render does this automatically)
- [ ] Review CORS_ALLOWED_ORIGINS
- [ ] Never commit .env files
- [ ] Use environment variables for sensitive data

## 📝 Monitoring

- Check email for Render alerts
- Monitor free tier usage in dashboard
- Keep eye on build logs for errors
- Set up error tracking (optional)

## 🆘 Getting Help

- Render docs: https://render.com/docs
- Django deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/
- Check Render logs for specific errors
- Test locally first with `python manage.py runserver`

---

**Deployment URL Pattern:**
- Backend API: `https://bgremover-api.onrender.com/api/process/`
- Frontend: `https://bgremover-frontend.onrender.com`

Replace service names with your actual names from Render dashboard.
