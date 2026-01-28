# Background Remover - AI-Powered Image Processing

A web application that removes image backgrounds using AI and applies custom colors or patterns.

## 🎯 Features

- **AI Background Removal**: Intelligent background detection using rembg library
- **Custom Background**: Apply solid colors or keep transparent background
- **Fast Processing**: Optimized for speed with automatic image downsampling
- **Easy Download**: Download processed images as PNG
- **Web-Based UI**: Simple, responsive interface with no installation needed

## 📋 Prerequisites

- **Python 3.12+** (tested on Python 3.12.3)
- **XAMPP or MySQL** server running on localhost:3306
- **pip** package manager

## 🚀 Quick Start

### 1. Clone/Setup

```bash
cd f:\bgremover
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install Django==5.0 djangorestframework==3.15.1 Pillow==10.2.0 numpy==1.26.4 rembg[onnx]==2.0.57 onnxruntime==1.17.1 mysqlclient==2.2.4
```

### 4. Setup Database

**Option A: Using XAMPP (Recommended)**
- Start XAMPP Control Panel
- Click "Start" for MySQL
- Open `http://localhost/phpmyadmin`
- Create new database: `bgremover`

**Option B: Command Line**
```bash
mysql -u root -p
CREATE DATABASE bgremover;
EXIT;
```

### 5. Run Backend

```bash
cd backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

**Output should show:**
```
Django version 5.0, using settings 'config.settings'
Starting development server at http://0.0.0.0:8000/
```

### 6. Run Frontend (New Terminal)

```bash
cd frontend
python -m http.server 3000 --bind 127.0.0.1
```

**Output should show:**
```
Serving HTTP on 127.0.0.1 port 3000 (http://127.0.0.1:3000/) ...
```

### 7. Open Browser

Navigate to: **http://127.0.0.1:3000**

## 📱 How to Use

1. **Upload Image**: Select JPG, PNG, WebP, BMP, GIF, or AVIF
2. **Choose Background Type**: 
   - **Color**: Solid background color (pick any color)
   - **Transparent**: Keep transparent background
3. **Select AI Model**: 
   - **BRIA**: Better for photos (slower)
   - **ISNet**: Faster, good for logos/graphics
4. **Click "Process Image"**: Wait for processing (1-2 minutes first time, faster after)
5. **Download**: Click "Download Image" to save PNG file

## 📂 Project Structure

```
bgremover/
├── backend/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── requirements.txt
│   ├── apps/
│   │   └── images/
│   │       ├── models.py
│   │       ├── views.py
│   │       ├── urls.py
│   │       ├── serializers.py
│   │       └── migrations/
│   └── config/
│       ├── settings.py
│       ├── urls.py
│       ├── wsgi.py
│       ├── cors_middleware.py
│       └── asgi.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── [static files]
│
└── README.md
```

## 🔧 API Endpoints

### Process Image
- **URL**: `POST /api/process/`
- **Request**:
  ```
  FormData:
    - image: File (JPG, PNG, WebP, BMP, GIF, AVIF)
    - background_type: string ("color" or "transparent")
    - background_value: string (hex color like "#FFFFFF")
  ```
- **Response**:
  ```json
  {
    "image": "data:image/png;base64,...",
    "status": "SUCCESS"
  }
  ```

## ⚡ Performance Tips

1. **First Run**: AI model downloads (~300MB), takes longer
2. **Image Size**: Automatically downsampled to 1024px for faster processing
3. **Model Selection**: ISNet is faster than BRIA
4. **Typical Time**: 
   - First run: 3-5 minutes (model download)
   - Subsequent runs: 30-60 seconds per image

## 🐛 Troubleshooting

### Can't reach http://127.0.0.1:3000
- Check if frontend server is running: `netstat -ano | findstr :3000`
- Restart frontend server with correct command (see section 6)
- Try different port: `python -m http.server 8080 --bind 127.0.0.1`

### Database Connection Error
- Ensure MySQL is running (check XAMPP Control Panel)
- Database name must be: `bgremover`
- Run: `python manage.py migrate` from backend folder

### "Processing... please wait" never completes
- Check Django terminal for errors
- First run downloads AI model (can take 5+ minutes)
- Try smaller image file
- Check available disk space (needs ~1GB for model)

### Image quality is poor
- Use JPG or PNG format (best quality)
- Try BRIA model instead of ISNet
- Upload larger image (min 300x300px recommended)

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 5.0 | Web framework |
| DRF | 3.15.1 | REST API |
| rembg[onnx] | 2.0.57 | AI background removal |
| Pillow | 10.2.0 | Image processing |
| onnxruntime | 1.17.1 | AI model inference |
| numpy | 1.26.4 | Numerical computing |
| mysqlclient | 2.2.4 | MySQL database driver |

## 📝 Notes

- This is a development setup (not for production)
- All images are processed locally - nothing is uploaded to cloud
- First run may take 5+ minutes while AI model downloads
- Processed images are returned as base64 data URLs

## 🎓 Technologies Used

- **Backend**: Django 5.0 + Django REST Framework
- **Frontend**: HTML5, CSS3, Vanilla JavaScript ES6+
- **AI**: rembg (RemBG library with ONNX models)
- **Database**: MySQL
- **Server**: Python built-in http.server

---

**Created**: January 2026  
**Status**: Development  
**Python**: 3.12+
