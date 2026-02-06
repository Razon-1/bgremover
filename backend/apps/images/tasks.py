from django.core.files.base import ContentFile
from .models import ImageJob
from .services import remove_background, add_background

def process_image_task(job_id):
    """Synchronous image processing (replaces Celery task)."""
    job = ImageJob.objects.get(id=job_id)

    try:
        image = job.original_image.read()
        fg = remove_background(image, job.model_used)
        final = add_background(fg, job.background_type, job.background_value)

        job.processed_image.save(
            f"result_{job.id}.png",
            ContentFile(final)
        )

        job.status = 'DONE'
        job.save()

    except Exception:
        job.status = 'FAILED'
        job.save()
