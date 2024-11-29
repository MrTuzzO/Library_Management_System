from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from users.models import UserProfile


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'id': 'required'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, balance=0.00)
        return user


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')