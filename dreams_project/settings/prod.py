
"""Production sozlamalari."""
import os

from django.core.exceptions import ImproperlyConfigured

from .base import *
from .base import DEFAULT_SECRET_KEY, SECRET_KEY

if SECRET_KEY == DEFAULT_SECRET_KEY:
    raise ImproperlyConfigured(
        "Production uchun SECRET_KEY muhit o'zgaruvchisini o'rnating."
    )

DEBUG = False

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if h.strip()
]

if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS ni o'rnating.")

CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if o.strip()
]

if not os.environ.get("DATABASE_URL"):
    raise ImproperlyConfigured("DATABASE_URL topilmadi!")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_CONTENT_TYPE_NOSNIFF = True
