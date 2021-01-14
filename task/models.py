from django.db import models
from django.urls import reverse
from PIL import Image


class ImageUpload(models.Model):
    name = models.TextField(blank=True)
    image = models.ImageField(upload_to='', blank=True)
    url_image = models.URLField(blank=True)
    prev_image = models.ImageField(upload_to='', blank=True)

    def get_absolute_url(self):
        return reverse('task:post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if args.__len__() != 0:
            super(ImageUpload, self).save(force_update=True)
            img = Image.open(self.image.path)
            size = (int(args[0]), int(args[1]))
            img.thumbnail(size)
            img.save(self.image.path)
        else:
            super(ImageUpload, self).save(*args, **kwargs)