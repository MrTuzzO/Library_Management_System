from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth import logout, update_session_auth_hash
from django.urls import reverse_lazy

from Library_Management_System import settings
from transactions.models import BorrowHistory
from . import forms
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail


def signup(request):
    if request.method == 'POST':
        signup_form = forms.RegistrationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('profile')
    else:
        signup_form = forms.RegistrationForm()

    return render(request, 'signup.html', {'form': signup_form, 'title': 'Sign Up'})


class UserLogin(LoginView):
    template_name = 'signup.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'You have successfully logged in!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please try again.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['title'] = 'Sign In'
        return contex


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        form = forms.EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been updated!')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})


@login_required
def deposit_money(request):
    if request.method == "POST":
        amount = request.POST.get('amount', None)
        if amount:
            amount = Decimal(amount)
            if amount > 0:
                profile = UserProfile.objects.get(user=request.user)
                profile.balance += amount
                profile.save()

                messages.success(request, f'Deposit of {amount} Taka successful!')
                subject = "Deposit Taka"
                message = f"Deposit of {amount} Taka successful!"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [profile.user.email]
                send_mail(subject, message, email_from, recipient_list)

                return redirect('profile')
            else:
                messages.error(request, 'Amount must be greater than zero.')
        else:
            messages.error(request, 'Please enter an amount.')
    return render(request, 'deposit_money.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')


@login_required
def profile(request):
    user = request.user
    borrow_history = BorrowHistory.objects.filter(user=user).order_by('-borrow_date')
    context = {
        'user': user,
        'borrow_history': borrow_history,
    }
    return render(request, 'profile.html', context)
