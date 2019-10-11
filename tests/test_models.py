
from django.test import TestCase
from books.models import Author, Book, Genre, Status

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non modified data for all class methods.
        Author.objects.create(first_name='Big', last_name='Bob')
    
    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')
        
    def test_last_name(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')
        
    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)
        
    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)
        
    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.first_name}, {author.last_name}'
        self.assertEquals(expected_object_name, str(author))
        
    def test_absolut_url(self):
        author = Author.objects.get(id=1)
        #this will also fail if the urlconf is not defined
        self.assertEquals(author.get_absolute_url(), '/books/author/1/')
        
        
class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_book = Book.objects.create(
                title='Hello, World?',
                summary='About everything',
                pub_house='Harper&Collins',
                category='pv',
                author=test_author,
                )
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        
        test_book.save()
        
    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)
        
    def test_summary_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('summary').max_length
        self.assertEquals(max_length, 1000)
        
    def test_pub_house_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('pub_house').max_length
        self.assertEquals(max_length, 200)
        
    def test_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.get_absolute_url(), '/books/book/1/')
       
from django.contrib.auth.models import User

class StatusModelTest(self):
    @classmethod
    def setUpTestData(self):
        
        # create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_book = Book.objects.create(
                title='Hello, World?',
                summary='About everything',
                pub_house='Harper&Collins',
                category='pv',
                author=test_author,
                )
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
        
        book_wisher = User.objects.create()
        
        status = Status.objects.create(book=test_book, wisher=book_wisher, due_back=)
        
        
            
    
    
    
    
    
    
        