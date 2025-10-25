# api/views.py
from rest_framework import generics, permissions # Добавляем permissions
from catalog.models import Genre, Language, Author, Book # Модели из catalog
from .serializers import ( # Наши сериализаторы из api.serializers
    GenreSerializer, LanguageSerializer, AuthorSerializer, BookSerializer
) 
# Импортируем наш кастомный permission, если будем его создавать позже
# from .permissions import IsOwnerOrReadOnly 

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]