from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<uuid:pk>/renew', views.renew_book_librarian, name='renew_book_librarian'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
    path('mybooks/', views.LoanedBooksListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.AllLoanedBooks.as_view(), name='all-borrowed'),
]
