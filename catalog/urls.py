from django.urls import path, include
import catalog.views as views


urlpatterns = [
    path('', views.index, name='index')
]