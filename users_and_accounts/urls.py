from django.urls import path, re_path, include

import users_and_accounts.views as views



urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('contact/', views.ContactFormAjaxView.as_view(), name="contact_form")
]
