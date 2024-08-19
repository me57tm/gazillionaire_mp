import random
import time

from pynput import keyboard as nput_keyboard
from game_controller import *
from TwitchPlays.TwitchPlays_Connection import Twitch


class Player:
    company_name = ""

    def __init__(self, name):
        self.company_name = name

    def run(self):
        # Run any commands needed for initial event menus, then call loop.
        raise NotImplementedError("Setup must overriden by child class for menus before the main menu.")

    def loop(self):
        raise NotImplementedError("Children must implement a loop loop.")


class HumanPlayer(Player):

    def __init__(self, name, hotkey):
        super().__init__(name)
        self.hotkey = hotkey

    def run(self):
        self.loop()

    def loop(self):
        # wait until num0 is pressed:
        # TODO: allow this to be any key
        def on_press(key):
            if hasattr(key, 'vk') and key.vk == 96:
                # Stop listener
                return False
            '''try:
                print('alphanumeric key {0} pressed'.format(
                    key.char))
            except AttributeError:
                print('special key {0} pressed'.format(
                    key))'''

        with nput_keyboard.Listener(
                on_release=on_press) as listener:
            listener.join()


class TwitchPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.menu = MainMenu()
        self.connection = Twitch()
        # input(">>>")
        self.connection.twitch_connect("jon_me57tm")
        self.messages = []
        self.connection.twitch_receive_messages()

    def run(self):
        burnt_messages = self.connection.twitch_receive_messages()
        self.loop()
        self.menu = MainMenu()

    def loop(self):
        while self.menu is not None:
            for message in self.messages:
                self.menu.run(message['message'])
                self.menu = self.menu.next_menu
                if self.menu is None:
                    break
            self.messages = self.connection.twitch_receive_messages()


class PyConsolePlayer(Player):
    menu = None

    def run(self):
        self.menu = MainMenu()
        self.loop()

    def loop(self):
        while self.menu is not None:
            self.menu.run(input(">>>").lower())
            self.menu = self.menu.next_menu


class MelonEnjoyer(Player):
    # An AI that LOVES cantaloupes. Not designed to execute an effective strategy, simply to get an AI working / be a
    # demonstration. I suspect it will go bankrupt quite quickly.
    passengerPrice = 0
    advertsSet = False
    phase = "buy"
    holding = ["polyester", "kryptoons", "x fuels"]

    def run(self):
        # sleep(10)
        self.loop()

    def loop(self):
        main = MainMenu()
        bank = BankMenu()
        loan = LoanMenu()
        advert = AdvertMenu()
        explore = ExploreMenu()
        special = SpecialMenu()
        market = MarketMenu()

        main.run("bank")
        bank.run("withdraw max")
        bank.run("back")
        main.run("loan")
        loan.run("borrow max")
        loan.run("back")
        main.run("pick")
        if self.passengerPrice == 0:
            PassengerMenu().run("set price 2500")
            self.passengerPrice = 2500
        PassengerMenu().run("back")
        main.run("ad")
        if not self.advertsSet:
            advert.run("passenger 2")
            advert.run("commodity 2")
        advert.run("place")
        advert.run("back")
        main.run("pay crew")
        main.run("pay tax")
        main.run("explore")
        explore.run("special")
        if special.tilo:
            special.run("gamble max")
            time.sleep(1)
            special.run("no")
            special.run("back")
        else:
            special.run("special")
        explore.run("back")
        main.run("buy fuel")
        main.run("marketplace")

        for item in self.holding:
            market.run("sell " + item)
        self.holding = []

        if self.phase == "buy":
            market.run("buy cantaloupe")
            self.phase = "sell"
        else:
            market.run("sell cantaloupe")
            self.phase = "buy"
        attempted = []
        while random.randint(1, 3) != 1:
            item = random.choice(ShopMenu.resources)
            if item not in attempted:
                market.run("buy " + item)
                attempted += item
            self.holding += item
        market.run("back")
        main.run("loan")
        loan.run("pay max")
        loan.run("back")
        main.run("zinn")
        ZinnMenu().run("pay max")
        ZinnMenu().run("back")
        main.run("travel")
        travel = TravelMenu()
        while travel.next_menu is not None:
            travel.run(random.choice(TravelMenu.PLANETS))
