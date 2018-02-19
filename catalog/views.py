import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView,
                                    UpdateView, DeleteView)
from django.urls import reverse, reverse_lazy

from .forms import RenewBookForm
from .models import Author, Book, BookInstance, Genre, Language

# Create your views here.
@permission_required('catalog.can_mark_returned')
@permission_required('catalog.can_edit')
@login_required
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'catalog/index.html', context)

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
        book_inst = get_object_or_404(BookInstance, pk=pk)

        if request.method == 'POST':
            form = RenewBookForm(request.POST)

            if form.is_valid():
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
                book_inst.due_back = form.cleaned_data['renewal_date']
                book_inst.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('catalog:all-borrowed') )

        # If this is a GET (or any other method) create the default form.
        else:
            proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
            form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

        return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = "Some data to be displayed!"
        return context

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin, ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author


    def get_queryset(self):
        return Author.objects.all().order_by('date_of_birth')


class LoanedBooksListView(LoginRequiredMixin, ListView):
    model =             BookInstance
    template_name =     'catalog/books_borrowed.html'
    paginate_by =       10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooks(PermissionRequiredMixin, ListView):
    model =             BookInstance
    template_name =     'catalog/all_borrowed_books.html'
    paginate_by =       10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
