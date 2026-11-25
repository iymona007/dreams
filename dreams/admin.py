from django.contrib import admin

from .models import Dream, DreamImage


class DreamImageInline(admin.TabularInline):
    model = DreamImage
    extra = 0


@admin.register(Dream)
class DreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'short_text', 'stage', 'category', 'visibility', 'images_count', 'created_at')
    list_filter = ('stage', 'category', 'visibility', 'created_at')
    search_fields = ('text', 'user__username')
    inlines = [DreamImageInline]

    @admin.display(description="Matn")
    def short_text(self, obj):
        return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text

    @admin.display(description="Rasmlar")
    def images_count(self, obj):
        return obj.images.count()
