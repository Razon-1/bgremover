from django.db import models

class ImageJob(models.Model):
    BACKGROUND_TYPES = [
        ('color', 'Color'),
        ('image', 'Image'),
    ]

    MODELS = [
        ('isnet', 'ISNet'),
        ('bria', 'BRIA RMBG'),
    ]

    STATUS = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('DONE', 'Done'),
        ('FAILED', 'Failed'),
    ]

    original_image = models.ImageField(upload_to='originals/')
    processed_image = models.ImageField(upload_to='processed/', null=True, blank=True)

    background_type = models.CharField(max_length=20, choices=BACKGROUND_TYPES)
    background_value = models.TextField()

    model_used = models.CharField(max_length=20, choices=MODELS)
    status = models.CharField(max_length=20, choices=STATUS, default='PENDING')

    file_size = models.BigIntegerField()
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)