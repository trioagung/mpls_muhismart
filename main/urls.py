
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('upload-logo/', views.upload_logo, name='upload_logo'),
    path('debug-media/', views.debug_media, name='debug_media'),
]
