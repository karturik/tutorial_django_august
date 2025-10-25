# api/serializers.py
from rest_framework import serializers
from catalog.models import Genre, Language, Author, Book # Импортируем нужные модели из catalog

# --- Сериализатор для Жанра ---
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        # Указываем поля, которые хотим включить в API
        # 'id' обычно добавляется автоматически ModelSerializer'ом, 
        # но явно указать не помешает.
        fields = ['id', 'name'] 

# --- Сериализатор для Языка ---
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'date_of_death',
            # Позже добавим сюда 'books'
            ] 
        
# --- Сериализатор для Книги ---
# class BookSerializer(serializers.ModelSerializer):
#     # --- Представление связей ---
#     # Способ 1: Использовать ID связанных объектов (по умолчанию для ForeignKey)
#     # author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all()) # Можно явно указать
#     # language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all()) # Можно явно указать
#     # genre = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all()) # many=True для ManyToMany

#     # Способ 2: Использовать строковое представление (__str__) связанных объектов
#     author = serializers.StringRelatedField(read_only=True) # read_only=True, т.к. создать автора по строке нельзя
#     language = serializers.StringRelatedField(read_only=True) # read_only=True
#     # Для ManyToMany StringRelatedField тоже работает, но только для чтения
#     genre = serializers.StringRelatedField(many=True, read_only=True) 

#     # Способ 3: Вложенные сериализаторы (покажем для примера, но может быть избыточно)
#     # author = AuthorSerializer(read_only=True) 
#     # language = LanguageSerializer(read_only=True)
#     # genre = GenreSerializer(many=True, read_only=True)

#     class Meta:
#         model = Book
#         fields = [
#             'id', 
#             'title', 
#             'author', # Имя поля должно совпадать с полем в модели
#             'summary', 
#             'isbn', 
#             'genre',  # Имя поля должно совпадать с полем в модели
#             'language', # Имя поля должно совпадать с полем в модели
#             'display_genre', # Можно включить метод модели, если он нужен
#             'get_absolute_url', # И URL тоже можно, хотя для API это менее типично
#         ]
#         # Можно также указать read_only_fields, если какие-то поля нельзя изменять через API
#         # read_only_fields = ['display_genre', 'get_absolute_url']

class BookSerializer(serializers.ModelSerializer):
    # Поля для записи (используют ID)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )
    language_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), source='language', write_only=True
    )
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genre', write_only=True, many=True
    )

    # Поля только для чтения (используют строковое представление)
    author = serializers.StringRelatedField(read_only=True)
    language = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(many=True, read_only=True)

    # Поле только для чтения, которое показывает ID связанных жанров (для информации)
    genre_ids_read = serializers.PrimaryKeyRelatedField(
        source='genre', read_only=True, many=True, help_text="IDs of related genres (read-only)"
    )


    class Meta:
        model = Book
        fields = [
            'id', 
            'title', 
            # Поля для чтения
            'author', 
            'language', 
            'genre', 
            # Поля для записи (будут видны в формах Browsable API)
            'author_id',
            'language_id',
            'genre_ids',
            # Дополнительные поля
            'summary', 
            'isbn', 
            'display_genre', # Метод модели
            'genre_ids_read', # ID жанров для чтения
            # 'get_absolute_url', 
        ]
        # Указывать read_only_fields не нужно, т.к. мы явно пометили поля для чтения