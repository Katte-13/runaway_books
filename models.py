from django.db import models
from django.urls import reverse #to generate URLS by reverse URL patterns
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction"""
    name = models.CharField(max_length=200)
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        """string for representing the Model object (in Admin site etc.) """
        return self.name
    
    
class Book(models.Model):
    """Model representing a book"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, blank=True)
    genre = models.ManyToManyField(Genre)
    pub_house = models.CharField(max_length=200)
    pub_date = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    CATEGORY = (
            ('r','roman'), 
            ('pv','povestiri'), 
            ('e','eseuri'),
            ('pz','poezie'), 
            ('nf','non-fiction'),
            ('t','teatru'))    
    
    category = models.CharField(max_length=2, choices=CATEGORY, blank=True)
    
    
    def display_genre(self):
       """Creates a string for the genre. This is required to display genre in Admin"""
       return ', '.join([genre.name for genre in self.genre.all()[:3]])
       
    display_genre.short_description = 'Genre'
   
    def __str__(self):
        """String for representing the Model object"""
        return self.title
    
    def get_absolute_url(self):
        return reverse('books:book_detail', args=[str(self.id)])
    
    
from datetime import date

class Status(models.Model):
    """Model representing the book status"""
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    wisher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    GIVEAWAY_STATUS = (
            ('av','Cu chef de ducă'), 
            ('wished', 'Dorită'), 
            ('gone','Pooof! Nu mai e!'))

    status = models.CharField(max_length=10, default='av', choices=GIVEAWAY_STATUS)
    
    class Meta:
        permissions = (("can_mark_wished", "Set book as wished"),)
        verbose_name_plural = "statuses"
        
    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['first_name', 'last_name']
    
    def get_absolute_url(self):
        return reverse('books:author_detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.first_name}, {self.last_name}'
    
