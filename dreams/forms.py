from django import forms

from .models import Dream, DreamImage


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    """Bir nechta rasm tanlash uchun maydon (Django hujjatidagi usul)."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={'accept': 'image/*'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_clean(item, initial) for item in data]
        return [single_clean(data, initial)] if data else []


class DreamForm(forms.ModelForm):
    images = MultipleImageField(required=False, label="Rasmlar")
    remove_images = forms.ModelMultipleChoiceField(
        queryset=DreamImage.objects.none(), required=False, label="Rasmlarni olib tashlash"
    )

    class Meta:
        model = Dream
        fields = ['text', 'stage', 'category', 'mood', 'visibility']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': "Orzuingizni shu yerga yozing... istagancha uzun bo'lishi mumkin",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['remove_images'].queryset = self.instance.images.all()
        else:
            del self.fields['remove_images']

    def clean(self):
        cleaned = super().clean()
        text = (cleaned.get('text') or '').strip()
        new_images = cleaned.get('images') or []
        kept = 0
        if self.instance.pk:
            removed = cleaned.get('remove_images')
            removed_ids = [img.pk for img in removed] if removed else []
            kept = self.instance.images.exclude(pk__in=removed_ids).count()
        if not text and not new_images and not kept:
            raise forms.ValidationError(
                "Orzu uchun matn yozing yoki kamida bitta rasm yuklang (yoki ikkalasini ham)."
            )
        cleaned['text'] = text
        return cleaned

    def save(self, commit=True):
        dream = super().save(commit=commit)
        if commit:
            self._save_images(dream)
        return dream

    def _save_images(self, dream):
        removed = self.cleaned_data.get('remove_images')
        if removed:
            for img in removed:
                img.image.delete(save=False)
                img.delete()
        start = dream.images.count()
        for offset, file in enumerate(self.cleaned_data.get('images') or []):
            DreamImage.objects.create(dream=dream, image=file, position=start + offset)
