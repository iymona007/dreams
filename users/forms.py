from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email (ixtiyoriy)")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('display_name', 'bio', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'maxlength': 300}),
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
        }
