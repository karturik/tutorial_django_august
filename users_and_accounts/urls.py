from django.urls import path, re_path, include

import catalog.views as views



urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]