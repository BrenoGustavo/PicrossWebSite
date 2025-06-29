from django.urls import path
from . import views

urlpatterns = [
    path('', views.daily_puzzle, name='daily_puzzle'),
    path('check/', views.check_solution, name='check_solution'),  # <- esta linha
]