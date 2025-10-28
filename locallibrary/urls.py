"""
URL configuration for locallibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("catalog/", include('catalog.urls')),
    path("user/", include('users_and_accounts.urls')),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('api.urls', namespace='api')),

    # --- Добавляем URL для документации API ---
    # Схема OpenAPI (обычно YAML или JSON файл)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI: интерактивный интерфейс для исследования и тестирования API
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc: альтернативный интерфейс для просмотра документации
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
