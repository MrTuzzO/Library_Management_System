from django.shortcuts import render, get_object_or_404, redirect
from transactions.models import BorrowHistory
from .models import Book, Category, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from transactions.models import BorrowHistory
from books.models import Book


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    has_borrowed = False

    if request.user.is_authenticated:
        has_borrowed = BorrowHistory.objects.filter(user=request.user, book=book).exists()

    return render(request, 'book_details.html', {
        'book': book,
        'reviews': reviews,
        'has_borrowed': has_borrowed,
    })


@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        review_text = request.POST['review_text']
        rating = int(request.POST['rating'])
        Review.objects.create(user=request.user, book=book, review_text=review_text, rating=rating)
        messages.success(request, 'Your review has been added!')
        return redirect('book_detail', book_id=book.id)

    return render(request, 'book_details.html', {'book': book})
