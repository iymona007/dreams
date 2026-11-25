from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import DreamForm
from .models import Dream


class FeedView(ListView):
    """Public feed: faqat ommaviy orzular, qidiruv va filtrlar bilan."""
    template_name = 'dreams/feed.html'
    context_object_name = 'dreams'
    paginate_by = 12

    def get_queryset(self):
        qs = (
            Dream.objects.public()
            .select_related('user')
            .prefetch_related('images')
        )
        params = self.request.GET
        q = params.get('q', '').strip()
        if q:
            qs = qs.filter(text__icontains=q)
        if params.get('category') in Dream.Category.values:
            qs = qs.filter(category=params['category'])
        if params.get('stage') in Dream.Stage.values:
            qs = qs.filter(stage=params['stage'])
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop('page', None)
        ctx.update({
            'q': self.request.GET.get('q', ''),
            'category': self.request.GET.get('category', ''),
            'stage': self.request.GET.get('stage', ''),
            'categories': Dream.Category.choices,
            'stages': Dream.Stage.choices,
            'qs': urlencode(params),
        })
        return ctx


class DreamDetailView(DetailView):
    template_name = 'dreams/dream_detail.html'
    context_object_name = 'dream'

    def get_queryset(self):
        # Private orzu boshqalarga 404 qaytaradi
        return (
            Dream.objects.visible_to(self.request.user)
            .select_related('user')
            .prefetch_related('images')
        )


class DreamCreateView(LoginRequiredMixin, CreateView):
    model = Dream
    form_class = DreamForm
    template_name = 'dreams/dream_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Orzuingiz joylandi! ✨")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Yangi orzu"
        return ctx


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user_id == self.request.user.id


class DreamUpdateView(OwnerRequiredMixin, UpdateView):
    model = Dream
    form_class = DreamForm
    template_name = 'dreams/dream_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Orzu yangilandi.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Orzuni tahrirlash"
        return ctx


class DreamDeleteView(OwnerRequiredMixin, DeleteView):
    model = Dream
    template_name = 'dreams/dream_confirm_delete.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        for img in self.object.images.all():
            img.image.delete(save=False)
        messages.success(self.request, "Orzu o'chirildi.")
        return super().form_valid(form)
