from django.shortcuts import render
from books.models import Book, Category


def home(request):
    category_id = request.GET.get('category', None)
    books = Book.objects.filter(categories__id=category_id) if category_id else Book.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'books': books, 'categories': categories})