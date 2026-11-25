from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from core.validators import validate_image_size


class Profile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    display_name = models.CharField("Ism", max_length=60, blank=True)
    bio = models.TextField("O'zim haqimda", max_length=300, blank=True)
    avatar = models.ImageField(
        "Avatar", upload_to='avatars/', blank=True, null=True, validators=[validate_image_size]
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

    def __str__(self):
        return f"Profil: {self.user}"

    @property
    def name(self):
        return self.display_name or self.user.username
