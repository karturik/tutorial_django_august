from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from django.shortcuts import render
from django.http.response import HttpResponse

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

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors
    }

    return render(
        request,
        'index.html',
        context=context
    )

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    queryset = Book.objects.filter(title__icontains='war')[:5]
    template_name = 'books/book_list_page.html'

    # def get_queryset(self) -> QuerySet[Any]:
    #     return Book.objects.filter(title__icontains='war')[:5]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(BookListView, self).get_context_data(**kwargs)

        context['some_data'] = 'This is just some data'
        return context
