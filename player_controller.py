import random
import time

from flask_socketio import emit
from pynput import keyboard as nput_keyboard
from game_controller import *
from TwitchPlays.TwitchPlays_Connection import Twitch
from flask_app import *



class Player:
    company_name = ""

    def __init__(self, name, ship):
        self.company_name = name
        self.ship = ship

    def run(self):
        # Run any commands needed for initial turn information menus, then call loop.
        raise NotImplementedError("Setup must overriden by child class for menus before the main menu.")

    def loop(self):
        # Run commands required to activate the main menu and its submenus, ends when you fly to another planet.
        raise NotImplementedError("Children must implement a main-menu loop.")

    def events(self):
        raise NotImplementedError("Children must implement an event chain")

    @staticmethod
    def click_ok_buttons():
        alerts_complete = False
        while not alerts_complete:
            GAME.click_input()  # Move the mouse out the way of any buttons so they can be found
            sleep(2)
            try:
                ok = locateOnScreen('ui_imgs/ok.png')
                click(ok)
            except:
                try:
                    click(locateOnScreen("ui_imgs/ok2.png"))
                except:
                    alerts_complete = True

    def auto_start_turn(self):
        GAME.click_input(coords=(600, 560))  # Click "Start Turn"
        self.click_ok_buttons()
        BottomButtonMenu(4).click_button(0)


class HumanPlayer(Player):

    def __init__(self, name, ship, hotkey):
        super().__init__(name, ship)
        self.hotkey = hotkey

    def run(self):
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
    def __init__(self, name, ship, channel="", condition=(lambda x: True), cutoff=0, one_player = False):
        super().__init__(name, ship)
        self.menu = MainMenu()
        self.connection = Twitch()
        self.connection.twitch_connect(channel)
        self.condition = condition
        self.cutoff = cutoff
        self.one_player = one_player
        self.connection.twitch_receive_messages()

    def run(self):
        self.connection.twitch_receive_messages()  # Burn unrelated old messages
        self.menu = MainMenu()
        self.auto_start_turn()
        self.loop()

    def get_commands(self):
        messages = self.connection.twitch_receive_messages()
        commands = []
        for message in messages:
            if self.condition(message):
                commands.append(message['message'].lower())
        if self.cutoff > 0:
            return commands[:self.cutoff]
        else:
            return commands

    def loop(self):
        commands = self.get_commands()
        while self.menu is not None:
            for command in commands:
                print("executing",command)
                self.menu.run(command)
                self.menu = self.menu.next_menu
                if self.menu is None:
                    break
            commands = self.get_commands()
        self.events()

    def events(self):
        print("event time")
        try:
            print("looking for an auction")
            locateOnScreen('ui_imgs/auction.png')
            am = AuctionMenu()
            chats_bid = 0
            print("one",self.one_player)
            if self.one_player:
                chats_bid = "hellothisisadummyvaluethatisn'tadigitsothewhileloopstartswhyareyoustillreadingit?"
                while not chats_bid.isdigit():
                    print("Waiting for a valid bid.....")
                    commands = self.get_commands()
                    if len(commands) > 0:
                        chats_bid = commands[0]
                    sleep(1)
            else:
                self.connection.twitch_receive_messages() # Burn non auction values
                print("Auction started... Letting chat cook.")
                sleep(30)
                actual_cutoff = self.cutoff
                self.cutoff = 0
                total_bids = 0
                for command in self.get_commands():
                    if command.isdigit():
                        chats_bid += int(command)
                        total_bids += 1
                chats_bid = chats_bid // total_bids
                self.cutoff = actual_cutoff
            print("Entering chat's bid...")
            am.run(str(chats_bid))
            #TODO: Maybe check that chat isn't bankrupt themselves

        except:
            print("there is no auction")
            pass
        print("flying")
        sleep(3)
        print("flying complete")

        myTurn = True
        while myTurn:
            GAME.click_input(coords=(30, 40))  # Move the mouse out the way of any buttons so they can be found
            try:
                locateOnScreen('ui_imgs/begin_turn.png')
                myTurn = False
                print("my turn ended")
            except:
                try:
                    locateOnScreen("ui_imgs/yes.png")
                    yesNo = True
                except:
                    yesNo = False

                if yesNo:
                    commands = self.get_commands()
                    if len(commands) > 0:
                        if commands[0][:3] == "yes":
                            click(locateOnScreen("ui_imgs/yes.png"))
                            sleep(2)
                        elif commands[0][:2] == "no":
                            click(locateOnScreen("ui_imgs/no.png"))
                            sleep(2)
                else:
                    print("automatically clicking ok")
                    self.click_ok_buttons()


class PyConsolePlayer(Player):
    menu = MainMenu()

    def run(self):
        self.menu = MainMenu()
        self.auto_start_turn()
        self.loop()

    def loop(self):
        while self.menu is not None:
            self.menu.run(input(">>>").lower())
            self.menu = self.menu.next_menu
        self.events()

    def events(self):
        print("event time")
        try:
            # AUCTIONS ASK YOU "ARE YOU SURE" SOMETIMES
            print("looking for an auction")
            locateOnScreen('ui_imgs/auction.png')
            am = AuctionMenu()
            i = ""
            while not i.isdigit():
                print("please enter auction amount")
                i = input(">>>")
                sleep(1)
            print("bidding", i)
            am.run(i)
        except:
            print("there is no auction")
            pass
        print("flying")
        sleep(3)
        print("flying complete")

        myTurn = True
        while myTurn:
            GAME.click_input()  # Move the mouse out the way of any buttons so they can be found
            print("Checking next event popup")
            try:
                locateOnScreen('ui_imgs/begin_turn.png')
                myTurn = False
                print("my turn ended")
            except:
                try:
                    locateOnScreen("ui_imgs/yes.png")
                    yesNo = True
                except:
                    yesNo = False

                if yesNo:
                    print("yes or no")
                    x = input(">>>").lower()
                    if "yes" in x:
                        click(locateOnScreen("ui_imgs/yes.png"))
                    elif "no" in x:
                        click(locateOnScreen("ui_imgs/no.png"))
                else:
                    print("automatically clicking ok")
                    self.click_ok_buttons()
                sleep(2)


class MelonEnjoyer(Player):
    # An AI that LOVES cantaloupes. Not designed to execute an effective strategy, simply to get an AI working / be a
    # demonstration. I suspect it will go bankrupt quite quickly.
    passengerPrice = 0
    advertsSet = False
    phase = "buy"
    holding = []

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
