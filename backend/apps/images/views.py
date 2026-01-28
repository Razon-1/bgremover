from rest_framework.generics import RetrieveAPIView
from .serializers import ImageJobSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from PIL import Image
import imghdr
import json

from .models import ImageJob
from .tasks import process_image_task
from .serializers import ImageJobSerializer



# =========================
# VALIDATION SETTINGS
# =========================

MAX_SIZE = 100 * 1024 * 1024  # 100MB
MAX_DIMENSION = 4096


def validate_image(file):
    # 1️⃣ File size check
    if file.size > MAX_SIZE:
        raise ValueError("File too large (max 100MB)")

    # 2️⃣ File type check
    file_type = imghdr.what(file)
    if file_type not in ['jpeg', 'png', 'webp', 'bmp', 'gif', 'avif']:
        raise ValueError("Unsupported file type")

    # 3️⃣ Resolution check (allowed but optimized later)
    img = Image.open(file)
    w, h = img.size
    if max(w, h) > MAX_DIMENSION:
        pass


# =========================
# API VIEW (OPTIMIZED FOR SPEED)
# =========================

@csrf_exempt
def process_image_view(request):
    """Process image - remove background and apply color (FAST)"""
    
    if request.method == 'OPTIONS':
        return JsonResponse({'status': 'ok'})
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=400)
    
    try:
        from rembg import remove
        from io import BytesIO
        import base64
        
        # Get uploaded file
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        
        image_file = request.FILES['image']
        bg_type = request.POST.get('background_type', 'color')
        bg_value = request.POST.get('background_value', '#FFFFFF')
        
        print(f"\n✅ Processing: {image_file.name} ({image_file.size} bytes)")
        
        # Validate
        try:
            validate_image(image_file)
        except ValueError as e:
            print(f"❌ Validation failed: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        
        # Load and optimize image
        print("   Loading image...")
        img = Image.open(image_file)
        original_size = img.size
        
        # OPTIMIZATION 1: Downsample large images for faster processing
        max_size = 1024  # Process at max 1024px (fast enough, good quality)
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            print(f"   Downsampled to {new_size} for faster processing...")
        
        # OPTIMIZATION 2: Remove background (fast inference)
        print("   Removing background (this is the slowest part)...")
        img_no_bg = remove(img)
        
        # Ensure RGBA
        if img_no_bg.mode != 'RGBA':
            img_no_bg = img_no_bg.convert('RGBA')
        
        # OPTIMIZATION 3: Upscale back to original size for display
        if img_no_bg.size != original_size:
            print(f"   Upscaling back to original size...")
            img_no_bg = img_no_bg.resize(original_size, Image.Resampling.LANCZOS)
        
        # Apply background
        print(f"   Applying {bg_type} background...")
        if bg_type == 'color':
            background = Image.new('RGB', img_no_bg.size, bg_value)
            background.paste(img_no_bg, mask=img_no_bg.split()[3])
            result_img = background
        else:
            result_img = img_no_bg
        
        # Convert to base64 with compression
        print("   Encoding...")
        buffer = BytesIO()
        result_img.save(buffer, format='PNG', optimize=True)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        print("✅ Done!\n")
        return JsonResponse({
            'image': f'data:image/png;base64,{img_base64}',
            'status': 'SUCCESS'
        })
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

# =========================
# JOB STATUS API
# =========================

class JobStatusView(RetrieveAPIView):
    queryset = ImageJob.objects.all()
    serializer_class = ImageJobSerializer
