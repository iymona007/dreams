from django.conf import settings
from django.core.exceptions import ValidationError


def validate_image_size(file):
    if file.size > settings.MAX_IMAGE_SIZE:
        mb = settings.MAX_IMAGE_SIZE // (1024 * 1024)
        raise ValidationError(f"Rasm hajmi {mb} MB dan oshmasligi kerak.")
