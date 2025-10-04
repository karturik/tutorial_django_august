from django.urls import path, re_path, include
import catalog.views as views



urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books')
]