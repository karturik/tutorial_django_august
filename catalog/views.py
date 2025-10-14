from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from django.urls import reverse
from django.shortcuts import render
from django.http.response import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, Author, BookInstance, Genre

# Create your views here.
def index(request) -> HttpResponse:
    """
    Home page view function
    """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(
        status__exact="a"
    ).count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits
    }

    return render(
        request,
        'index.html',
        context=context
    )

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    queryset = Book.objects.all()
    template_name = 'books/book_list_page.html'

    paginate_by = 1

    # def get_queryset(self) -> QuerySet[Any]:
    #     return Book.objects.filter(title__icontains='war')[:5]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(BookListView, self).get_context_data(**kwargs)

        context['some_data'] = 'This is just some data'
        return context
    

class BookDetailView(generic.DetailView):
    model = Book
    template_name = "books/book_detail.html"

    def get_context_data(self, **kwargs):
        book_id = str(self.get_object().id)
        session_key = f'book_detail_page_num_visits_{book_id}'
        context = super().get_context_data(**kwargs)
        context['num_visits'] = self.request.session[session_key]
        return context
    
    def get(self, request, *args, **kwargs):
        book_id = str(self.get_object().id)
        session_key = f'book_detail_page_num_visits_{book_id}'
        num_visits = request.session.get(session_key, 0)
        request.session[session_key] = num_visits + 1
        return super().get(request, *args, **kwargs)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = "books/bookinstance_list_borrowed_user.html"
    paginate_by = 10
    login_url = "/user/accounts/login"

    def get_queryset(self) -> QuerySet[Any]:
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact="o").order_by('due_back')
