from django.contrib import admin

from .models import Book, Author, Genre, Status

"""Minimal registration of Models:
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Status)
"""

#class BooksInline(admin.TabularInline):
#    model = Book
#    extra = 0
    
@admin.register(Author)   
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
#    inlines = [BooksInline]

class StatusInline(admin.TabularInline):
    model = Status
    extra = 0
    
  
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'owner', 'display_genre')
    inlines = [StatusInline]

    
admin.site.register(Book, BookAdmin) 

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'wisher', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
            (None, {'fields': ('book',)}),
            ('Availability', {'fields': ('status', 'due_back', 'wisher')
            }),
           )
      
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
