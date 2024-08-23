from player_controller import *

player1 = PyConsolePlayer("AA")
player2 = PyConsolePlayer("BB")
player3 = PyConsolePlayer("CC")
player4 = PyConsolePlayer("DD")

players = [player1,player2,player3,player4]
#player1.menu = MainMenu()
#player1.events()
while True:
    print("player 1")
    player1.run()