from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from .models import Game
from .serializers import (
    UserSerializer,
    LoginSerializer,
    GameSerializer
)
import uuid

User = get_user_model()


class UserRegistrationAPIView(APIView):
    permission_classes= (AllowAny,)
    
    def get(self, request):
        # users = User.objects.all()
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data).is_valid()
        print(">>>>>>>>>>>",serializer)
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not username or not password or not email or not first_name or not last_name:
            return Response({'error': 'Please enter username, password, email, first_name, last_name'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        try:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            # password = User.objects.set_password(password)
            user.save()
        except:
            return Response({'error': 'Unable to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class UserUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None 

    def get(self, request, pk):
        try:
            user = self.get_user(pk=pk)
            if user:
                serializer = UserSerializer(user)
                return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        
        user = self.get_user(pk)
        if user:
            print(user, request.user, request.user.is_superuser, request.user.is_staff)
            # if user == request.user or request.user.is_superuser or request.user.is_staff:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                new_password = serializer.validated_data.pop('password', None)
                if new_password is not None:
                    user.set_password(new_password)
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user = self.get_user(pk)
        if user:
            if request.user.is_superuser or request.user == user:
                user.delete()
                return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'You are not authorized to delete this user.'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

 
class LoginAPIView(APIView):
    permission_classes= (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'token': access_token}, status=status.HTTP_200_OK)


class CreateGame(APIView):
    def post(self, request):
        game_id=str(uuid.uuid1().hex[:6])
        print("-=-=-=-=-=",request.user)
        game = Game(user=request.user, game_string="", game_id=game_id)
        game.save()
        return Response({"game_id": game.game_id}, status=status.HTTP_201_CREATED)

class GetBoard(APIView):
    def get(self, request, game_id):
        game = Game.objects.get(game_id=game_id)
        return Response({"game_string": game.game_string})

class UpdateBoard(APIView):
    def post(self, request, game_id):
        game = Game.objects.get(game_id=game_id)
        game.game_string += request.data['character']
        # Add logic to add random numbers
        game.save()
        return Response(status=status.HTTP_200_OK)

class ListGames(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
