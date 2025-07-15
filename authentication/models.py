from django.db import models

# Create your models here.

class InputImage(models.Model):
    image = models.ImageField(upload_to='images/')
    original_image = models.ImageField(upload_to='images/original/', blank=True)
    augmented_image = models.ImageField(upload_to='images/augmented/', blank=True)

    def __str__(self):
        return self.image.name