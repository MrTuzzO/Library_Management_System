from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Library_Management_System import settings
from .models import BorrowHistory
from books.models import Book
from users.models import UserProfile
from django.utils.timezone import now


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    profile = UserProfile.objects.get(user=request.user)
    if profile.balance < book.borrowing_price:
        messages.error(request, 'Insufficient balance!')
        return redirect('book_detail', book_id=book.id)
    profile.balance -= book.borrowing_price
    profile.save()
    BorrowHistory.objects.create(user=request.user, book=book, amount=book.borrowing_price)
    messages.success(request, 'Book borrowed successfully!')

    subject = "Borrowed Book"
    message = f"Borrowed {book.title}, Charged {book.borrowing_price}. You have {profile.balance} in your account."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [profile.user.email]
    send_mail(subject, message, email_from, recipient_list)

    return redirect('profile')


@login_required
def return_book(request, borrow_id):
    borrow = get_object_or_404(BorrowHistory, id=borrow_id, user=request.user, return_date__isnull=True)
    profile = UserProfile.objects.get(user=request.user)
    profile.balance += borrow.amount
    profile.save()
    borrow.return_date = now()
    borrow.save()
    messages.success(request, 'Book returned successfully!')
    return redirect('profile')
