from player_controller import *
import threading
from flask_app import *


# player1 = HumanPlayer("HumanPlayer", "the globulizer","")
# player1 = PyConsolePlayer("","")
# player2 = TwitchPlayer("Bingus Bongus", "mantagon")

# players = [player1]#, player2]#,player3,player4]
# player1.menu = MainMenu()
# player1.loop()

def main_loop():
    player1 = HumanPlayer("me57tm", "locomotis", "")

    players = [player1]
    currentPlayer = player1

    while True:
        print("Current Player:", currentPlayer.company_name)
        currentPlayer.run()
        sleep(0.2)
        currentPlayer = None
        for player in players:
            try:
                locateOnScreen("ui_imgs/ships/" + player.ship + ".png")
                currentPlayer = player
            except Exception as e:
                print(e)


loop = threading.Thread(target=main_loop)
loop.start()
socketio.run(app,allow_unsafe_werkzeug=True)
