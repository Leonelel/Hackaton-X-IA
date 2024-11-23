from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main chatbox view
    path('reset/', views.reset, name='reset'),  # Reset view
]