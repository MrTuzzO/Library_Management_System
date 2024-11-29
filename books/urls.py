from django.urls import path
from . import views

urlpatterns = [
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/add_review/', views.add_review, name='add_review'),
]
