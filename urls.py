from django.urls import path
from django.conf import settings

from .import views

app_name = 'books'

urlpatterns =[
        path('', views.index, name='index'),
        path('books/', views.BookListView.as_view(), name='books'),
        path('book/<int:pk>/', views.BookDetail.as_view(), name='book_detail'),
        path('authors/', views.AuthorListView.as_view(), name='authors'),
        path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),]


urlpatterns += [
        path('mybooks/', views.WishedBooksByUserListView.as_view(), name='my_wished'),
        path('myview/', views.WishedBooksAllUsersListView.as_view(), name='myview'),
        path('book/<int:pk>/renew/', views.renew_book_librarian, name='renew_book_librarian'),
        path('book/<int:pk>/status/', views.wish_book, name = 'status')]

urlpatterns += [
        path('authors/create/', views.AuthorCreate.as_view(), name='author_create'),
        path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
        path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
        ]

