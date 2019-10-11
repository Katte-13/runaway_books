import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views import generic, View
from django.forms import formset_factory

from .models import Book, Author, Genre, Status
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from books.forms import RenewBookModelForm, WishBookModelForm
# Create your views here.

def index(request):
    
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    num_available_books = Status.objects.filter(status__exact = 'av').count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    context = {
            'num_books': num_books,
            'num_authors': num_authors,
            'num_available_books': num_available_books,
            'num_visits': num_visits}
    
    return render(request, 'books/index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'books/book_list.html'
    paginate_by = 20
    
"""
class BookDetailView(generic.DetailView):
    model = Book
    template = 'books/book_detail.html'

"""
class BookDisplay(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookDisplay, self).get_context_data(**kwargs)
        context['form'] = WishBookModelForm()
        return context

class WishBook(SingleObjectMixin, FormView):
    form_class = WishBookModelForm()
    model = Status
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        self.object['wisher'] = request.user
        self.object['due_back'] = datetime.today()+datetime.datetime(days=10)
        self.object.save()
        return super(WishBook, self).post(request, *args, **kwargs)
        
    def get_success_url(self):
        return reverse('books:book_detail', kwargs={'pk':self.object.pk})
   
class BookDetail(View):
    def get(self, request, *args, **kwargs):
        view = BookDisplay.as_view()
        return view(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        view = WishBook.as_view()
        return view(request, *args, **kwargs)

class AuthorListView(generic.ListView):
    model= Author
    template_name = 'books/author_list.html'
    paginate_by = 20
 
    
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'books/author_detail.html'

    
class WishedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = Status
    template_name = 'books/status_list_whished_user.html'
    paginate_by = 20
    
    
    def get_queryset(self):
        return Status.objects.filter(wisher=self.request.user).filter(status__exact='wished').order_by('due_back')
    

class WishedBooksAllUsersListView(PermissionRequiredMixin, generic.ListView):
    model = Status
    permission_required = 'can_mark_wished'
    template_name = 'books/status_list_whished_all_users.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Status.objects.filter(status__exact='wished').order_by('due_back')

#Librariens can renew the wishing status
@permission_required('can_mark_wished')
def renew_book_librarian(request, pk):
    status = get_object_or_404(Status, pk=pk)
    
    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)
        
        if form.is_valid():
            status.due_back = form.cleaned_data['due_back']
            status.save() 
            return HttpResponseRedirect(reverse('books:myview'))
        
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(days=10)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})
        
    
    return render (request, 'books/renew_book_librarian.html', 
                   context = {'form': form, 'status': status})

#authenticated users can select the book they want to get
def wish_book(request, pk):
    status = get_object_or_404(Status, pk=pk)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = WishBookModelForm(request.POST)
        
        # Check if the form is valid:
        if form.is_valid():
            status.status = form.cleaned_data['status']
            status.due_back = datetime.date.today() + datetime.timedelta(days=10)
            status.wisher = request.user
            status.save()    
            # redirect to a new URL:        
            return HttpResponseRedirect(reverse('books:my_wished'))
    # If this is a GET (or any other method) create the default form
    else:
        form = WishBookModelForm()
        
    return render(request, 'books/status.html', 
                      context={'form': form, 'status': status})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    template_name_suffix = '_create_form'
   
class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'
    template_name_suffix = '_update_form'
    
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('books:authors')
    

