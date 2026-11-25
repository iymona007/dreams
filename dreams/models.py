from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.models import TimeStampedModel
from core.validators import validate_image_size


class DreamQuerySet(models.QuerySet):
    def public(self):
        return self.filter(visibility=Dream.Visibility.PUBLIC)

    def visible_to(self, user):
        """Ommaviy orzular + (kirgan bo'lsa) foydalanuvchining o'z private orzulari."""
        if user.is_authenticated:
            return self.filter(
                models.Q(visibility=Dream.Visibility.PUBLIC) | models.Q(user=user)
            )
        return self.public()


class Dream(TimeStampedModel):
    class Stage(models.TextChoices):
        IDEA = 'idea', "💭 Fikr"
        STARTED = 'started', "🌱 Boshladim"
        IN_PROGRESS = 'in_progress', "🚀 Harakatdaman"
        ACHIEVED = 'achieved', "🏆 Amalga oshdi"

    class Category(models.TextChoices):
        TRAVEL = 'travel', "✈️ Travel"
        CAREER = 'career', "💻 Career"
        LIFESTYLE = 'lifestyle', "🏡 Lifestyle"
        EDUCATION = 'education', "📚 Education"
        PERSONAL = 'personal', "💗 Personal"

    class Mood(models.TextChoices):
        CALM = 'calm', "🌙 Sokin"
        MAGIC = 'magic', "✨ Sehrli"
        JOY = 'joy', "🌈 Quvnoq"
        PASSION = 'passion', "🔥 Ishtiyoqli"
        PEACE = 'peace', "🌿 Tinch"

    class Visibility(models.TextChoices):
        PUBLIC = 'public', "🌍 Hamma ko'radi"
        PRIVATE = 'private', "🔒 Faqat men"

    STAGE_STEPS = [("💭", "Fikr"), ("🌱", "Boshladim"), ("🚀", "Harakatdaman"), ("🏆", "Amalga oshdi")]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dreams'
    )
    text = models.TextField("Orzu matni", blank=True)
    stage = models.CharField("Bosqich", max_length=20, choices=Stage.choices, default=Stage.IDEA)
    category = models.CharField("Kolleksiya", max_length=20, choices=Category.choices, blank=True)
    mood = models.CharField("Kayfiyat", max_length=20, choices=Mood.choices, blank=True)
    visibility = models.CharField(
        "Ko'rinishi", max_length=10, choices=Visibility.choices, default=Visibility.PUBLIC
    )
    achieved_at = models.DateTimeField(null=True, blank=True)

    objects = DreamQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Orzu"
        verbose_name_plural = "Orzular"
        indexes = [
            models.Index(fields=['visibility', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        preview = (self.text[:40] + '...') if len(self.text) > 40 else self.text
        return f"{self.user} - {preview or 'rasmli orzu'}"

    def save(self, *args, **kwargs):
        if self.stage == self.Stage.ACHIEVED and not self.achieved_at:
            self.achieved_at = timezone.now()
        elif self.stage != self.Stage.ACHIEVED:
            self.achieved_at = None
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dream_detail', kwargs={'pk': self.pk})

    @property
    def is_private(self):
        return self.visibility == self.Visibility.PRIVATE

    @property
    def stage_index(self):
        return self.Stage.values.index(self.stage)

    @property
    def journey(self):
        idx = self.stage_index
        return [
            {'emoji': e, 'label': label, 'done': i <= idx, 'line_done': i < idx}
            for i, (e, label) in enumerate(self.STAGE_STEPS)
        ]


class DreamImage(TimeStampedModel):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='dreams/%Y/%m/', validators=[validate_image_size])
    caption = models.CharField(max_length=200, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['position', 'id']
        verbose_name = "Orzu rasmi"
        verbose_name_plural = "Orzu rasmlari"

    def __str__(self):
        return f"Rasm #{self.pk} ({self.dream_id})"
