from django.db import models
from django.core.files.storage import default_storage
from apps.tools.compressor import *

# Create your models here.


class Banner(models.Model):
    image = models.ImageField(upload_to='banner')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Banner'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}: {self.image.url}"

    def save(self, *args, **kwargs):
        try:
            old_instance = Banner.objects.get(pk=self.pk)
            if self.image != old_instance.image:
                if old_instance.image:
                    default_storage.delete(old_instance.image.path)
                # Compress the new image
                self.image = compress_image(self.image, 50)
        except:  # Create mode
            if self.image:
                self.image = compress_image(self.image, 50)
        super().save(*args, **kwargs)
