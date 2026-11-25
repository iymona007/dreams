from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, UpdateView

from dreams.models import Dream

from .forms import ProfileForm, RegisterForm
from .models import Profile

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Xush kelibsiz! Ro'yxatdan o'tdingiz.")
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileView(ListView):
    """Foydalanuvchi sahifasi: boshqalar faqat ommaviy, egasi hammasini ko'radi."""
    template_name = 'users/profile.html'
    context_object_name = 'dreams'
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        self.profile_user = get_object_or_404(
            User.objects.select_related('profile'), username=kwargs['username']
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (
            Dream.objects.visible_to(self.request.user)
            .filter(user=self.profile_user)
            .prefetch_related('images')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        visible = self.get_queryset()
        ctx['profile_user'] = self.profile_user
        ctx['total'] = visible.count()
        ctx['achieved'] = visible.filter(stage=Dream.Stage.ACHIEVED).count()
        return ctx


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Profil yangilandi.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})
