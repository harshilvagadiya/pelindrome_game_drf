"""Implement REST APls for a palindrome game.
The following APls need to be implemented using Python
Django and Postman or any similar tool can be used for
testing.

Please use your preferred DB and design APl names

User APls
User get all user, creation, deletion and update.
These APls will be used for user management.
loggedin user can update only his information 
User Login.
Once a user login, then the user can invoke the Game
and List functionality.

Game APls
Start/Create
This will initialize empty string
This should return game-lD

getBoard
This will return the value string from the server.
e.g. after create-game, the state of the string will be".
and after the user invokes updateBoard, the string will
have some value.

updateBoard
Using this API, the user will append one character
between 'a' to 'z to string.
Server should update the string and add one more
and add more rendom number

once the leangth of the string is 6, it should return whether the string is pelindrome or not and


List of Games API

this api should list all game IDS created in system"""