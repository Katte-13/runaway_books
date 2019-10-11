from django.test import TestCase

import datetime
from django.utils import timezone

from django.urls import reverse
from books.models import Book, Author, Genre, Status

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestClass(cls):
        #create 23 authors for pagination test
        number_of_authors = 23
        
        for author_id in range(number_of_authors):
            Author.objects.create(
                    first_name = f'Christian {author_id}',
                    last_name = f'surname {author_id}')
            
        
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/books/authors')
        self.assertEqual(response.status_code, 200)
        
    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('books:authors'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_templates(self):
        response = self.client.get(reverse('books:authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books:author_list.html')
        
    def test_pagination_is_twenty(self):
        response = self.client.get(reverse('books:authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 20)
        
    def test_list_all_authors(self):
        #get second page and confirm it has exactly 3 items
        response = self.client.get(reverse('books:authors')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 3)
        
class BooksListViewTest(TestCase):
    @classmethod
    def setUpTestClass(cls):
        #create a list of 23 books
        number_of_books = 23
        #create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_book = Book.objects.create(
                author=test_author,
                genre=test_genre,
                title='Good-by!',
                summary='Abracadabra')
        for book_id in number_of_books:
            test_book(book_id)
    
        #create genre as a post-step
        genre_objects_for_book = Genre.objects.all
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
            
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/books/books/')
        self.assertEqual(response.status_code, 200)
        
    def test_view_accesible_by_name(self):
        response = self.client.get(reverse('books:books'))
        self.assertEqual(response.status_code, 200)
        
    def test_correct_template(self):
        response = self.client.get(reverse('books:books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        
    def test_pagination_is_twenty(self):
        response = self.client.get(reverse('books:books'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['book_list']) == 20)

    def test_list_all_books(self):
        response = self.client.get(reverse('books:books')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['book_list']) == 3)
            
            
            
from django.contrib.auth.models import User

class WishedBooksByUserListViewTest(TestCase):
    def setUp(self):
        #create 2 users
        test_user1 = User.objects.create(username='test_user1', password='stgr4ao/56')
        test_user2 = User.objects.create(username='test_user2', password='bn56dpt^4d')
        
        test_user1.save()
        test_user2.save()
        
        #create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_book = Book.objects.create(
                title='Good By!',
                author=test_author,
                summary='Abracadabra',
                genre=test_genre)
            
        #create genre as a post-step
        genre_objects_for_book = Genre.objects.all
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
            
        # create 30 Status objects
        
        number_of_book_copies = 30
        for book_copy in number_of_book_copies:
            allowed_time = timezone.today()+datetime.timedelta(days=book_copy%5)
            the_wisher = test_user1 if book_copy%2 else test_user2
            status = 'wished'
            Status.objects.create(
                    book = book_copy,
                    due_back = allowed_time,
                    wisher = the_wisher,
                    status = status )
        
            
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('books:my_wished'))
        self.assertRedirects(response, 'accounts/login/?next=/books/my_wished')
        
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='stgr4ao/56')
        response = self.client.get(reverse('books:my_wished'))
        
        self.assertEqual(str(response.context['user'], 'testuser1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/status_list_wished_user.html')
        
    def test_only_wished_books_in_list(self):
        login = self.client.login(username='testuser1', password='stgr4ao/56')
        response = self.client.get(reverse('books:my_view'))
        
        #check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        #check we have a response "success"
        self.assertEqual(response.status_code, 200)
        
        #check that initially we don't have any book in list
        self.assertTrue('status' in response.context)
        self.assertEqual(len(response.context['status']), 0)
        
        #now change every book to be wished
        books = Status.objects.all()[:10]
        
        for book in books:
            book.status = 'wished'
            book.save()
    
            
        #check that now we have wished books in the list
        response =  self.client.get(reverse('books:my_wished'))
        #check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        #check we have a response success
        self.assertTrue(response.status_code, 200)
        
        self.assertTrue('status_list' in response.context)
        
        # confirm all books belongs to testuser1 and are in list            
        for bookitem in response.context('status'):
            self.assertEqual(response.context['user'], bookitem.wisher)
            self.assertTrue('av', bookitem.status)
            
    def test_pages_ordered_by_due_date(self):
        #change all books to be all wished
        for book in Status.objects.all():
            book.satus = 'wished'
            book.save()
        
        login = self.client.login(username='test_user1', password='stgr4ao/56')
        response = self.client.get(reverse('books:my_wished'))
        
        #check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        #check that we have a response success
        self.assertEqual(response.status_code, 200)

        #confirm that of the items, only 20 are diplayed due to the pagination
        self.assertEqual(len(response.context['status']), 20)

        last_date = 0
        for book in response.context('status'):
            if last_date == 0:
                last_date == book.due_back
                
        else:
            self.assertTrue(last_date <= book.due_back)
            last_date = book.due_back
            
from django.contrib.auth.models import Permission

class RenewBookLibrarianTest(TestCase):
     
    def setUp(self):
        
        test_user1 = User.objects.create(username='testuser1', password='stgr4ao/56')
        test_user2 = User.objects.create(username='testuser2', password='bn56dpt^4d')
        
        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name = 'Set book as wished')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_book = Book.objects.create(
                title='Good By!',
                author=test_author,
                summary='Abracadabra')
            
        
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
        
        #Create a status for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_status1 = Status.objects.create(
                book = test_book,
                due_back = return_date,
                wisher = test_user1,
                status = 'wished')
        
        #create a status for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_status2 = Status.objects.create(
                book = test_book,
                due_back = return_date,
                wisher = test_user2,
                status = 'wished')
        
        
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('books:renew_book_librarian', kwargs={'pk': self.test_status1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith('accounts/login/'))
        
    def test_redirect_if_logged_in_but_no_correct_permission(self):
        login = self.client.login(username='testuser1', password='stgr4ao/56')
        response = self.client.get(reverse('books:myview', kwargs={'pk': self.test_status1.pk}))
        self.assertEqual(response.status_code, 403)
        
    def test_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='bn56dpt^4d')
        response = self.client.get(reverse('books:renew_book_librarian', kwargs={'pk': self.test_status2.pk}))
        self.assertEqual(response.status_code, 200)
        
    def test_uses_correct_templates(self):
        login = self.client.login(username='testuser2', password='bn56dpt^4d')
        response = self.client.get(reverse('books:renew_book_librarian', kwargs={'pk': self.test_status2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/renew_book_librarian.html')
        
    def test_form_renewal_date_initially_has_date_10_days_in_future(self):
        login = self.client.login(username='testuser2', password='bn56dpt^4d')
        response = self.client.get(reverse('books:renew_book_librarian', kwargs={'pk': self.test_status2.pk}))
        self.assertEqual(response.status_code, 200)
        
        date_10_days_in_future = datetime.date.today() + datetime.timedelta(days=10)
        self.assertEqual(response.context['form'].initial['due_back'], date_10_days_in_future)
        
    def test_redirects_to_wished_books_on_success(self):
        login = self.client.login(username='testuser2', password='bn56dpt^4d')
        valid_date_in_future = datetime.date.today()+datetime.timedelta(days=5)
        response = self.client.post(reverse('books:renew_book_librarian', kwargs={'pk', self.test_status2.pk,}),
                                    {'due_back': valid_date_in_future})
        self.assertRedirects(response, reverse('books:myview'))
        
    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='bn56dpt^4d')
        date_in_past = datetime.date.today() + datetime.timedelta(days=8)
        response = self.client.post(reverse('books:renew_book_librarian', kwargs={'pk': self.test_status2.pk,}), 
                                            {'due_back': date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'due-back', 'Data invalidă - dată aflată în trecut.')
        
    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='bn56dpt^4d')
        date_in_future = datetime.date.today() + datetime.timedelta(days=11)
        response = self.client.post(reverse('books:renew_book_librarian', kwargs={'pk': self.test_status2.pk,}), 
                                    {'due_back': date_in_future})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'due_back', 'Dată invalidă - mai mult de 10 zile.')

class WishBookTest(TestCase):
    
    def setUp(self):
        
        test_user = User.objects.create(username='testuser1', password='stgr4ao/56')
        test_user.save()
        
        test_author = Author.objects.create(first_name = 'John', last_name = 'Smith')
        test_genre = Genre.objects.create(name = 'Fantasy')
        test_book = Book.objects.create(
                title='Good By!',
                author=test_author,
                summary='Abracadabra')
        
        genre_object_for_book = Genre.objects.all()
        test_book.genre.set(genre_object_for_book)
        test_book.save()
        
        return_date = datetime.date.today()+datetime.timedelta(days=10)
        self.test_status = Status.objects.create(
                 book = test_book,
                 due_back = return_date,
                 wisher = test_user,
                 status = 'av')
        
    def test_user_not_logged(self):
        response = self.client.get(reverse('books:status', kwargs={'pk': self.test_status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, 'accounts/login/?next=/books/books/')
        
    def test_correct_template(self):
        response = self.client.get(reverse('books:status', kwargs={'pk': self.test_status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response, 'books/status.html')
        
    def test_redirects_to_wished_books_on_success(self):
        response = self.client.post(reverse('books:status', kwargs={'pk': self.test_status.pk}))
        self.assertRedirects(response, reverse('books:my_wished'))
    
import unittest
from django.test import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_details(self):
        response = self.client.get('/books/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['book_list']) == 20)
        
        
        
        
        
        
