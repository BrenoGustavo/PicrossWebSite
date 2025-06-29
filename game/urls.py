from django.urls import path
from . import views

urlpatterns = [
    path('', views.daily_puzzle, name='daily_puzzle'),
    path('random/', views.jogo_aleatorio, name='random_challenge'),
    path('check/', views.check_solution, name='check_solution'),  # <- esta linha

]