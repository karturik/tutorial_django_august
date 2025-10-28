# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken_views
from . import views # Импортируем представления из текущего приложения (api)

# # Имя для пространства имен URL (не обязательно для DRF, но хорошая практика)
# app_name = 'api' 

# urlpatterns = [
#     # Эндпоинты для Жанров (Genres)
#     path('genres/', views.GenreList.as_view(), name='genre-list'), 
#     path('genres/<int:pk>/', views.GenreDetail.as_view(), name='genre-detail'),

#     # Эндпоинты для Языков (Languages)
#     path('languages/', views.LanguageList.as_view(), name='language-list'),
#     path('languages/<int:pk>/', views.LanguageDetail.as_view(), name='language-detail'),

#     # Эндпоинты для Авторов (Authors)
#     path('authors/', views.AuthorList.as_view(), name='author-list'),
#     path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),

#     # Эндпоинты для Книг (Books)
#     path('books/', views.BookList.as_view(), name='book-list'),
#     path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),

#     # Можно добавить эндпоинт для корневого API, если нужно (пока пропустим)
# # path('' views.api_root), # Потребуется создать представление api_root
# ]

# # format_suffix_patterns - опционально, позволяет добавлять суффиксы типа .json, .api
# # В современных API это используется реже, чаще полагаются на заголовки Accept.
# # from rest_framework.urlpatterns import format_suffix_patterns
# # urlpatterns = format_suffix_patterns(urlpatterns) 

# Создаем экземпляр маршрутизатора
# DefaultRouter автоматически создает корневое представление API (API Root)
router = DefaultRouter() 

# Регистрируем наши ViewSets в маршрутизаторе
# router.register(префикс_url, ViewSet_класс, basename)
router.register(r'genres', views.GenreViewSet, basename='genre')
router.register(r'languages', views.LanguageViewSet, basename='language')
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'books', views.BookViewSet, basename='book')

# URL-паттерны теперь генерируются автоматически маршрутизатором.
# Нам нужно только включить сгенерированные URL в наши urlpatterns.
app_name = 'api' # Оставляем для ясности

urlpatterns = [
    # Включаем URL, сгенерированные router
    path('', include(router.urls)),
    path('token-auth/', authtoken_views.obtain_auth_token, name='api_token_auth') 
]

# Ручное определение URL-паттернов больше не нужно, если используем Router
# urlpatterns = [
#     path('genres/', views.GenreList.as_view(), name='genre-list'), 
#     ... и т.д. ...
# ]