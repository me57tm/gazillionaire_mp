from player_controller import *

#Start turn ship is not the same size as other menus, it's smaller. darn.

player1 = HumanPlayer("AA", "")
player2 = TwitchPlayer("BB")

while True:
    print("player 1")
    player1.run()
    print("player 2")
    player2.run()