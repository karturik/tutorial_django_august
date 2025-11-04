from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        # Указываем поля, которые должны быть в форме
        fields = ['name', 'email', 'message'] 
        # Можно добавить виджеты для настройки полей ввода, если нужно
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}), 
        }
