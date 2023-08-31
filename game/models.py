from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username
    
class Game(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.CharField(max_length=100, unique=True)
    game_string = models.CharField(max_length=100)
    is_palindrome = models.BooleanField(default=False)
