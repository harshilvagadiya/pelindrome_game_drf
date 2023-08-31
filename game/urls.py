from django.urls import path
from .views import (
    UserRegistrationAPIView,
    LoginAPIView,
    UserUpdateDeleteAPIView,
    GameList, GameStart, GameBoard

)

urlpatterns = [
    path('users/login/', LoginAPIView.as_view(), name='users-login'),
    path('users/register/', UserRegistrationAPIView.as_view(), name='users-register'),
    path('users/get_all_user/', UserRegistrationAPIView.as_view(), name='all-users'),
    path('users/get/<int:pk>/', UserUpdateDeleteAPIView.as_view()),
    path('users/update/<int:pk>/', UserUpdateDeleteAPIView.as_view()),
    path('users/delete/<int:pk>/', UserUpdateDeleteAPIView.as_view()),
    path('games/', GameList.as_view(), name='game-list'),
    path('games/start/', GameStart.as_view(), name='game-start'),
    path('games/board/<str:game_id>/', GameBoard.as_view(), name='game-board'),
    
    
]
