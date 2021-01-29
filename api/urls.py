from django.urls import path
from .views.books import fetchBooks

urlpatterns = [
    path('books',fetchBooks)
]
