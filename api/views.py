# api/views.py
from rest_framework import generics, permissions, viewsets # Добавляем permissions
from django_filters import rest_framework as filters
from catalog.models import Genre, Language, Author, Book # Модели из catalog
from .serializers import ( # Наши сериализаторы из api.serializers
    GenreSerializer, LanguageSerializer, AuthorSerializer, BookSerializer
) 
# Импортируем наш кастомный permission, если будем его создавать позже
from .permissions import IsStaffOrReadOnly 

class GenreList(generics.ListCreateAPIView):
    """
    API endpoint для просмотра списка жанров или создания нового жанра.
    """
    queryset = Genre.objects.all() # Какие объекты используем
    serializer_class = GenreSerializer # Какой сериализатор применяем
    # Разрешения: Читать могут все, создавать - только аутентифицированные
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint для просмотра, обновления или удаления конкретного жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # Разрешения: Читать могут все, изменять/удалять - только аутентифицированные
    # Позже можно добавить более гранулярные права (например, только админ)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

class LanguageList(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

class LanguageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --- Представления для Book ---
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]

    # --- Переопределение для связи с пользователем (если нужно) ---
    # Если бы мы хотели, чтобы поле 'owner' (или похожее) автоматически 
    # устанавливалось на текущего пользователя при создании книги через API,
    # мы бы переопределили метод perform_create:
    # def perform_create(self, serializer):
    #     # serializer.save(owner=self.request.user) 
    #     # Но у нас в модели Book нет поля owner, это просто пример
    #     serializer.save() # Стандартное сохранение

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]


class GenreViewSet(viewsets.ModelViewSet):
    """
    Этот ViewSet автоматически предоставляет действия `list`, `create`, 
    `retrieve`, `update` и `destroy` для Жанров.
    """
    queryset = Genre.objects.all().order_by('name') # Хорошо бы добавить сортировку
    serializer_class = GenreSerializer
    permission_classes = [IsStaffOrReadOnly] # Применяем ко всем действиям
    filterset_fields = ['name']

# --- ViewSet для Language ---
class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all().order_by('name')
    serializer_class = LanguageSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['name']

# --- ViewSet для Author ---
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('last_name', 'first_name')
    serializer_class = AuthorSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['last_name']

# --- ViewSet для Book ---
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]

    # Если нужно переопределить какое-то действие, можно сделать так:
    # def perform_create(self, serializer):
    #     # Дополнительная логика при создании
    #     # serializer.save(owner=self.request.user) # Пример
    #     serializer.save()

    # Можно также добавлять кастомные действия с помощью декоратора @action
    # @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    # def mark_as_read(self, request, pk=None):
    #     # Логика для кастомного действия
    #     ...
    filterset_fields = {
        'language': ['exact'], # Точное совпадение по ID языка (?language=1)
        'genre': ['exact'],    # Точное совпадение по ID жанра (?genre=2)
        # Для поиска по названию нужно будет настроить более сложный фильтр или использовать SearchFilter
        'title': ['icontains'], # Поиск по частичному совпадению без учета регистра (?title__icontains=Джейн)
    }
    # Альтернатива: Использование SearchFilter для более простого поиска
    # from rest_framework import filters as drf_filters
    # filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter]
    # filterset_fields = ['language', 'genre'] # Оставляем фильтры по связям
    # search_fields = ['title', 'summary', 'author__first_name', 'author__last_name'] # Поля для поиска