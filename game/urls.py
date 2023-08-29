from django.urls import path
from .views import (
    UserRegistrationAPIView,
    LoginAPIView,
    UserUpdateDeleteAPIView,
    CreateGame, GetBoard, UpdateBoard, ListGames
)

urlpatterns = [
    path('users/login/', LoginAPIView.as_view(), name='users-login'),
    path('users/register/', UserRegistrationAPIView.as_view(), name='users-register'),
    path('users/get_all_user/', UserRegistrationAPIView.as_view(), name='all-users'),

    path('users/get/<int:pk>/', UserUpdateDeleteAPIView.as_view()),
    path('users/update/<int:pk>/', UserUpdateDeleteAPIView.as_view()),
    path('users/delete/<int:pk>/', UserUpdateDeleteAPIView.as_view()),
    
    path('games/create/', CreateGame.as_view()),
    path('games/<str:game_id>/board/', GetBoard.as_view()),
    path('games/<str:game_id>/update/', UpdateBoard.as_view()),
    path('games/list/', ListGames.as_view()),
    
    
]
