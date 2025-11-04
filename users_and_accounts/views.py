import json

from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from django.views.generic.edit import FormView

from .forms import ContactForm


# Представление для самой страницы регистрации (оставляем как было или адаптируем)
class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('catalog') # Укажите ваш URL для перенаправления

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

# --- Наше AJAX представление ---
def validate_username(request):
    """
    Проверяет, существует ли пользователь с таким именем (регистронезависимо).
    Ожидает GET-параметр 'username'.
    Возвращает JSON: {'is_taken': true/false}.
    """
    # Получаем значение параметра 'username' из GET-запроса.
    # request.GET - это словарь с параметрами GET-запроса.
    # .get('username', None) - безопасный способ получить значение,
    # вернет None, если параметр отсутствует.
    username = request.GET.get('username', None)

    if username is None:
        # Желательно обрабатывать случай, когда параметр не передан
        return JsonResponse({'error': 'Username parameter missing'}, status=400)

    # Проверяем наличие пользователя в базе данных.
    # User.objects.filter(username__iexact=username) - ищет пользователя.
    # __iexact - регистронезависимое точное совпадение.
    # .exists() - возвращает True, если найден хотя бы один объект, иначе False.
    is_taken = User.objects.filter(username__iexact=username).exists()

    # Формируем данные для ответа
    data = {
        'is_taken': is_taken
    }
    # Возвращаем ответ в формате JSON.
    # JsonResponse автоматически установит правильный Content-Type: application/json.
    return JsonResponse(data)

# def contact_form_view(request: HttpRequest):
#     # Если запрос НЕ AJAX, просто отображаем пустую форму
#     # Метод is_ajax() устарел, проверяем заголовок HTTP_X_REQUESTED_WITH
#     # Этот заголовок обычно добавляют JavaScript-библиотеки (как jQuery) или его нужно добавлять вручную при использовании Fetch
#     is_ajax_request = request.headers.get("X-Requested-With") == "XMLHttpRequest"

#     if request.method == 'POST':
#         # Создаем экземпляр формы и заполняем его данными из POST-запроса
#         form = ContactForm(request.POST)

#         if form.is_valid():
#             # Данные формы валидны
#             instance = form.save() # Сохраняем объект ContactMessage в БД
#             # Для AJAX возвращаем JSON с сообщением об успехе и именем пользователя
#             if is_ajax_request:
#                 return JsonResponse({
#                     "message": f"Спасибо, {instance.name}! Ваше сообщение получено.",
#                     "name": instance.name # Можно вернуть и другие данные при необходимости
#                     }, status=200)
#             else:
#                 # Обычный POST-запрос не через AJAX - можем сделать редирект или показать страницу успеха
#                 return redirect('index') # Замените на ваш URL
#                 # return render(request, 'contact_success.html', {'name': instance.name})

#         else:
#             # Данные формы невалидны
#             if is_ajax_request:
#                 # Для AJAX возвращаем ошибки формы в формате JSON и статус 400 (Bad Request)
#                 # form.errors.as_json() возвращает строку JSON, ее и передаем
#                 return JsonResponse({"errors": form.errors}, status=400)
#             else:
#                 # Для обычного POST-запроса просто рендерим форму снова с ошибками
#                 return render(request, 'contact_form.html', {'form': form})

#     # Если это GET-запрос (или любой другой метод, не POST)
#     else:
#         form = ContactForm() # Создаем пустую форму

#     # Отображаем шаблон с формой
#     return render(request, 'contact_form.html', {'form': form})

class ContactFormAjaxView(FormView):
    template_name = 'contact_form.html' # Тот же шаблон
    form_class = ContactForm
    # success_url = reverse_lazy('some-success-url') # Нужен для НЕ-AJAX случаев, если не переопределять form_valid/form_invalid полностью

    def form_valid(self, form):
        """ Вызывается, если форма валидна. """
        instance = form.save()
        # Проверяем, был ли запрос сделан через AJAX
        is_ajax_request = self.request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if is_ajax_request:
            # Если AJAX, возвращаем JSON
            return JsonResponse({
                "message": f"Спасибо, {instance.name}! Ваше сообщение получено (из CBV).",
                "name": instance.name
                }, status=200)
        else:
             # Если не AJAX, вызываем стандартное поведение (редирект на success_url)
            return super().form_valid(form)

    def form_invalid(self, form):
        """ Вызывается, если форма невалидна. """
        is_ajax_request = self.request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if is_ajax_request:
            # Если AJAX, возвращаем ошибки в JSON
             return JsonResponse({"errors": form.errors}, status=400)
        else:
            # Если не AJAX, вызываем стандартное поведение (повторный рендер шаблона с ошибками)
            return super().form_invalid(form)