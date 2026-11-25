from django.db import models


class TimeStampedModel(models.Model):
    """Barcha modellar uchun umumiy: yaratilgan va yangilangan vaqt."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
