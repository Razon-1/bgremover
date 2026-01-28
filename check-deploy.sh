#!/bin/bash
# Deployment checklist for Render

echo "🚀 Deployment Checklist for Render"
echo "===================================="
echo ""

# Check Python version
echo "✓ Python version:"
python --version
echo ""

# Check required files
echo "✓ Required files:"
for file in "backend/Procfile" "backend/manage.py" "backend/requirements.txt" "frontend/index.html" "DEPLOY_RENDER.md"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (MISSING)"
    fi
done
echo ""

# Check environment variables file
echo "✓ Environment file:"
if [ -f ".env.example" ]; then
    echo "  ✅ .env.example exists"
else
    echo "  ❌ .env.example (create one)"
fi
echo ""

# Check settings.py configuration
echo "✓ Django settings:"
if grep -q "dj_database_url" backend/config/settings.py; then
    echo "  ✅ dj_database_url imported"
else
    echo "  ❌ dj_database_url not found"
fi

if grep -q "load_dotenv" backend/config/settings.py; then
    echo "  ✅ python-dotenv configured"
else
    echo "  ❌ python-dotenv not configured"
fi
echo ""

# Check git status
echo "✓ Git status:"
git status --short
echo ""

# Reminders
echo "📋 Before deploying to Render:"
echo "  1. Generate a secure SECRET_KEY:"
echo "     python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
echo ""
echo "  2. Push all changes to GitHub:"
echo "     git push origin main"
echo ""
echo "  3. Create Render services (see DEPLOY_RENDER.md)"
echo ""
echo "  4. Update frontend API URL after backend deployment"
echo ""
echo "✅ All checks complete!"
