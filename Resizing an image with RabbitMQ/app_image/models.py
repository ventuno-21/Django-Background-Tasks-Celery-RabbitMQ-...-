from django.db import models

# Create your models here.


class UploadedImage(models.Model):
    # store uploaded image
    image = models.ImageField(upload_to="uploads/")

    # store processed image path (After any changes/resize on an uploaded image)
    processed_image = models.ImageField(upload_to="processed/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"
