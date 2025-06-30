from django.urls import path
from . import views

urlpatterns = [
    path('', views.daily_puzzle, name='daily_puzzle'),
    path('check_daily/', views.check_daily, name='check_daily'),
    
    path('random/', views.jogo_aleatorio, name='random_challenge'),
    path('check_random/', views.check_random, name='check_random'),

    path('generate/', views.generate_grid, name='generate_grid'),
]