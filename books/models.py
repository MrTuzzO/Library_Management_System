from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='book_images/')
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    rating = models.PositiveIntegerField(default=1)
    review_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/5)"