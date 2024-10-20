from pywinauto import Application, keyboard
from pyautogui import locateOnScreen, ImageNotFoundException, click
# from pydirectinput import click
from time import time, sleep

app = None
while app is None:
    try:
        app = Application().connect(path='Gazillionaire.exe')
    except:
        print("Could not find game, please open it!")
        sleep(5)
GAME = app.Gazillionaire.wait('ready')
GAME.move_window(x=None, y=None, width=776, height=609)


class Menu:
    global GAME
    commands = ["x", "close", "screenshot"]
    next_menu = None

    def __init__(self):
        self.next_menu = self

    def run(self, command):
        command_parts = command.split(" ")
        command = command_parts[0]
        args = []
        if command in self.commands:
            if len(command_parts) > 1:
                args = command_parts[1:]
            self._execute(command, args)

    # It is recommended to use the pre-processing command loop to call execute rather than calling execute directly
    def _execute(self, command, args=[]):
        if command == "x" or command == "close":
            self.close_pop_up()
        elif command == "screenshot":
            GAME.capture_as_image().save('screenshots/Gazillionaire' + str(int(time())) + '.png')

    @staticmethod
    def btn_location(menu_start, menu_end, buffer, total_buttons, button_number):
        if button_number >= total_buttons or button_number < 0:
            raise IndexError
        return menu_start + buffer + button_number * ((menu_end - menu_start) // total_buttons)

    @staticmethod
    def close_pop_up():
        try:
            xbuttoncoords = locateOnScreen('ui_imgs/x.png')
            click(xbuttoncoords)
            click(
                xbuttoncoords)  # Sometimes the button doesn't get clicked even though the mouse moves so we click twice
            success = True
        except ImageNotFoundException:
            try:
                xbuttoncoords = locateOnScreen('ui_imgs/inverted_x.png')
                click(xbuttoncoords)
                click(xbuttoncoords)
                GAME.click_input()
                success = True
            except ImageNotFoundException:
                success = False
        return success

    def money_menu(self, amount):
        if amount == "max" or amount == "all":
            GAME.click_input(coords=(460, 370))
        else:
            try:
                int(amount)
                keyboard.send_keys(amount)
            except ValueError:
                pass
        GAME.click_input(coords=(400, 435))
        return not self.close_pop_up()

    def __str__(self):
        return str(self.commands)


class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.commands = self.commands + [
            "marketplace", "market",
            "supply",
            "warehouse",
            "passengers", "pick", "passenger",
            "advertise", "ad", "advert",
            "pay",
            "buy",
            "explore",
            "stocks", "stock",
            "bank",
            "loan",
            "zinn", "zinns",
            "journey", "travel", "leave",
        ]

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        match command:
            case "marketplace" | "market":
                GAME.click_input(coords=(350, 150))
                self.next_menu = MarketMenu()
            case "supply":
                GAME.click_input(coords=(500, 150))
                self.next_menu = SupplyMenu()
            case "warehouse":
                GAME.click_input(coords=(600, 150))
                self.next_menu = WarehouseMenu()
            case "journey" | "travel" | "leave":
                GAME.click_input(coords=(150, 150))
                self.next_menu = TravelMenu()
            case "stock" | "stocks":
                GAME.click_input(coords=(200, 350))
                self.next_menu = StocksMenu()
            # case "money:
            # game.click_input(coords=(200, 400))
            case "bank":
                GAME.click_input(coords=(200, 450))
                self.next_menu = BankMenu()
            case "loan":
                GAME.click_input(coords=(200, 500))
                self.next_menu = LoanMenu()
            case "zinn" | "zinns":
                GAME.click_input(coords=(200, 550))
                self.next_menu = ZinnMenu()
            case "pick" | "passenger" | "passengers":
                GAME.click_input(coords=(500, 250))
                GAME.click_input(coords=(325, 550))
                self.close_pop_up()
                self.next_menu = PassengerMenu()
            case "advert" | "advertise" | "ad":
                GAME.click_input(coords=(500, 300))
                self.next_menu = AdvertMenu()
            case "pay":
                if len(args) > 0:
                    if args[0] == "crew" or args[0] == "wages":
                        GAME.click_input(coords=(500, 350))
                        crew_menu = TwoButtonEventMenu()
                        crew_menu.run("right")
                        self.close_pop_up()
                        crew_menu.run("left")
                    elif args[0] == "tax" or args[0] == "taxes":
                        GAME.click_input(coords=(500, 400))
                        GAME.click_input(coords=(450, 530))
                        self.close_pop_up()
                        GAME.click_input(coords=(250, 530))
                    elif args[0] == "zinn":
                        GAME.click_input(coords=(200, 550))
                        zinn = ZinnMenu()
                        # if len(args) >

            case "buy":
                if len(args) > 0:
                    if args[0] == "insurance":
                        GAME.click_input(coords=(500, 450))
                        insurance_menu = TwoButtonEventMenu()
                        insurance_menu.run("right")
                        self.close_pop_up()
                        insurance_menu.run("left")
                    elif args[0] == "fuel":
                        # Open Menu
                        GAME.click_input(coords=(720, 100))
                        # Attempt to buy max amount of fuel
                        GAME.click_input(coords=(600, 550))
                        GAME.click_input(coords=(400, 400))
                        if self.close_pop_up():
                            # We failed to buy fuel, attempt to buy minimum amount of fuel
                            GAME.click_input(coords=(600, 550))
                            GAME.click_input(coords=(340, 340))
                            GAME.click_input(coords=(400, 400))
                            self.close_pop_up()
                        # Go back to main menu
                        GAME.click_input(coords=(450, 550))
            case "explore":
                GAME.click_input(coords=(500, 500))
                self.next_menu = ExploreMenu()

    def __str__(self):
        return "Main Menu\nValid Commands:\njourney/travel/leave\nmarket\nsupply\nwarehouse\nstocks\nbank\nloan\nzinn" \
               "\npick/passenger\nadvertise/advert/ad\npay <wages/crew/tax>\nbuy <insurance/fuel>\nexplore"


class TwoButtonEventMenu(Menu):
    def __init__(self):
        super().__init__()
        self.commands = self.commands + [
            "yes", "left",
            "no", "right"
        ]

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if command == "yes" or command == "left":
            GAME.click_input(coords=(480, 525))
        elif command == "no" or command == "right":
            GAME.click_input(coords=(580, 525))


class BottomButtonMenu(Menu):
    num_buttons = 1
    ycoord = 575

    def __init__(self, num_buttons):
        super().__init__()
        self.num_buttons = num_buttons
        self.commands = self.commands + ["back"]

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if command == "back":
            self.close_pop_up()
            self.click_button(0)
            self.next_menu = MainMenu()

    def click_button(self, number):
        buttons_start = 24
        buttons_end = 696
        spacer = 50
        GAME.click_input(coords=(
            Menu.btn_location(buttons_start, buttons_end, spacer, self.num_buttons, number), self.ycoord))


class BankMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(5)
        self.commands = self.commands + ["deposit", "withdraw"]

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if len(args) > 0:
            if command == "deposit":
                if args[0] == "max":
                    self.click_button(2)
                else:
                    self.click_button(1)
                    self.money_menu(args[0])
            elif command == "withdraw":
                if args[0] == "max":
                    self.click_button(4)
                else:
                    self.click_button(3)
                    self.money_menu(args[0])

    def __str__(self):
        return "Bank Menu\nValid Commands:\ndeposit <amount/max>\nwithdraw <amount/max>\nback"


class LoanMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(5)
        self.commands = self.commands + ["pay", "borrow"]

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if len(args) > 0:
            if command == "pay":
                if args[0] == "back" and len(args) > 1:
                    args[0] = args[1]
                if args[0] == "max":
                    self.click_button(2)
                else:
                    self.click_button(1)
                    self.money_menu(args[0])
            elif command == "borrow":
                if args[0] == "max":
                    self.click_button(4)
                else:
                    self.click_button(3)
                    self.money_menu(args[0])

    def __str__(self):
        return "Trader's Union Menu\nValid Commands:\npay <amount/max>\nborrow <amount/max>"


class ZinnMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(3)
        self.commands = self.commands + ["pay"]

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if len(args) > 0:
            if command == "pay":
                if args[0] == "back" and len(args) > 1:
                    args[0] = args[1]
                if args[0] == "max":
                    self.click_button(2)
                else:
                    self.click_button(1)
                    self.money_menu(args[0])

    def __str__(self):
        return "Zinn's Menu\nValid Commands:\npay <amount/max>\nback"


class StocksMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(6)
        self.commands = self.commands + ["buy", "sell", "show"]

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if len(args) > 0:
            if command == "buy":
                self.click_button(1)
                self.money_menu(args[0])
            elif command == "sell":
                self.click_button(2)
                self.money_menu(args[0], False)
            elif command == "show" and args[0] == "shares":
                self.click_button(5)

    def money_menu(self, amount, buying=True):
        # The stock market requires its own money menu as the buttons
        # are too far away from the others to be interchangable
        if amount == "max":
            if buying:
                GAME.click_input(coords=(460, 370))
            else:
                GAME.click_input(coords=(470, 380))
        else:
            try:
                int(amount)
                keyboard.send_keys(amount)
            except ValueError:
                pass
        if buying:
            GAME.click_input(coords=(390, 410))
        else:
            GAME.click_input(coords=(390, 450))

    def __str__(self):
        return "Stock Market Menu\nValid Commands:\nbuy <amount/max>\nsell <amount/max>\nshow shares\nback"


class PassengerMenu(BottomButtonMenu):
    ycoord = 550

    def __init__(self):
        super().__init__(3)
        self.commands = self.commands + ["set"]

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if len(args) > 0 and command == "set":
            if args[0] == "ticket" or args[0] == "price" and len(args) > 1:
                if args[1] == "price" and len(args) > 2:
                    args[0] = args[2]
                else:
                    args[0] = args[1]
            self.click_button(2)
            self.money_menu(args[0])

    def money_menu(self, amount):
        if amount == "max" or amount == "all":
            GAME.click_input(coords=(450, 330))
        else:
            try:
                int(amount)
                keyboard.send_keys(amount)
            except ValueError:
                pass
        GAME.click_input(coords=(380, 400))
        return not self.close_pop_up()

    def __str__(self):
        return "Passengers Menu\nValid Commands:\nset price <amount/max>\nback"


class AdvertMenu(TwoButtonEventMenu):
    def __init__(self):
        super().__init__()
        self.commands = self.commands + ["passenger", "commodity", "place", "back"]

    def _execute(self, command, args=[]):
        super()._execute(command)
        if command == "back":
            self.close_pop_up()
            self._execute("left")
            self.next_menu = MainMenu()
        elif command == "place":
            self._execute("right")
        elif len(args) > 0:
            if command == "passenger":
                GAME.click_input(coords=(150, 100))
            elif command == "commodity":
                GAME.click_input(coords=(250, 100))
            try:
                button_num = int(args[0])
                if button_num < 0:
                    button_num = 0
                if button_num > 6:
                    button_num = 6
                GAME.click_input(coords=(200, 150 + button_num * 64))
            except ValueError:
                pass
            self._execute("right")

    def __str__(self):
        return "Advert Menu\nValid Commands:\npassenger <0-6>\ncommodity <0-6>\nplace\nback"


class ExploreMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(6)
        self.commands = self.commands + ["special", "weather", "news"]

    def _execute(self, command, args=[]):

        super()._execute(command, args)
        if command == "special":
            self.click_button(1)
            if not self.close_pop_up():
                self.next_menu = SpecialMenu()
        elif command == "weather":
            self.click_button(2)
            sleep(5)
            TwoButtonEventMenu().run("left")
        elif command == "news":
            self.click_button(3)
            sleep(5)
            TwoButtonEventMenu().run("left")

    def __str__(self):
        return "Explore Menu\nValid Commands:\nspecial\nweather\nnews"


class SpecialMenu(TwoButtonEventMenu):
    tilo = False
    gambling = False

    def __init__(self):
        super().__init__()
        self.commands = self.commands + ["back", "special"]
        self.commands.remove("yes")
        self.commands.remove("no")
        try:
            locateOnScreen('ui_imgs/tilo_special.png')
            self.tilo = True
            self.commands.remove("special")
            self.commands = self.commands + ["gamble"]
        except:
            self.tilo = False

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if self.gambling:
            if command == "yes":
                GAME.click_input(coords=(350, 420))
            elif command == "no":
                GAME.click_input(coords=(430, 430))
                self._execute("back")

            try:
                locateOnScreen('ui_imgs/x.png')
            except:
                sleep(1)
                self.next_menu = ExploreMenu()
                self.gambling = False
                self._execute("left")
        else:
            if command == "back":
                Menu.close_pop_up()
                self._execute("left")
                self.next_menu = ExploreMenu()
            elif command == "special":
                self._execute("right")
                sleep(4)
                self.next_menu = ExploreMenu()
                self._execute("left")
            elif len(args) > 0 and command == "gamble":
                self._execute("right")
                self.money_menu(args[0])
                try:
                    locateOnScreen('ui_imgs/x.png')
                    self.gambling = True
                    self.commands.remove("gamble")
                    self.commands.remove("back")
                    self.commands = self.commands + ["yes", "no"]
                except:
                    sleep(3)
                    self.next_menu = ExploreMenu()
                    self._execute("left")

    def money_menu(self, amount):
        if amount == "max" or amount == "all":
            GAME.click_input(coords=(450, 340))
        else:
            try:
                int(amount)
                keyboard.send_keys(amount)
            except ValueError:
                pass
        GAME.click_input(coords=(400, 400))

    def __str__(self):
        if self.gambling:
            return "Special Menu\nValid Commands:\nyes\nno"
        elif self.tilo:
            return "Special Menu\nValid Commands:\ngamble <amount/max>\nback"
        else:
            return "Special Menu\nValid Commands:\nspecial\nback"


class TravelMenu(BottomButtonMenu):
    PLANETS = []

    def __init__(self):
        super().__init__(3)
        if TravelMenu.PLANETS == []:
            print("Finding planets...")
            i = 0
            for planet in ["bass", "frac", "hork", "loro", "mira", "nosh", "ooom", "pyke", "queg", "stye", "tilo",
                           "vexx", "xeen", "zile"]:
                if i == 7:
                    break
                try:
                    locateOnScreen('ui_imgs/planets/' + planet + '.png')
                    TravelMenu.PLANETS.append(planet)
                    i += 1
                except:
                    pass
        if len(TravelMenu.PLANETS) != 7:
            print("FAILURE HOW COULD THIS BE")
            print(TravelMenu.PLANETS)
        self.commands = self.commands + ["distance", "facilities"] + TravelMenu.PLANETS

    def _execute(self, command, args=[]):
        super()._execute(command)
        if command == "distance":
            self.click_button(1)
            self.next_menu = FacilitiesMenu()
        elif command == "facilities":
            self.click_button(2)
            self.next_menu = FacilitiesMenu()
        elif command in TravelMenu.PLANETS:
            # Deposit our cash to gain interest.
            self._execute("back")
            main = MainMenu()
            bank = BankMenu()
            main.run("bank")
            bank.run("deposit max")
            bank.run("back")
            main.run("journey")
            # sleep to ensure the menu is actually open
            sleep(0.3)
            # now we're back on the travel menu, actually go to the planet
            planet_location = locateOnScreen('ui_imgs/planets/' + command + '.png')
            click(planet_location)
            sleep(1)
            if not self.close_pop_up():
                # TODO: this should be none for the main script to handle, but err, there is not main script.
                self.next_menu = None

    def __str__(self):
        return_string = "Travel Menu\nValid Commands:\ndistance\nfacilities"
        for planet in TravelMenu.PLANETS:
            return_string += planet + "\n"
        return return_string + "back"


class FacilitiesMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(3)
        self.commands += ["planet", "distance", "facilities"]

    def _execute(self, command, args=[]):
        super()._execute(command)
        if command == "back":
            self.next_menu = TravelMenu()
        elif command == "distance":
            self.click_button(1)
        elif command == "facilities":
            self.click_button(2)
        elif command == "planet" and len(args) > 0:
            menu_start = 41
            menu_end = 530
            buffer = 50
            try:
                args[0] = int(args[0])
            except ValueError:
                args[0] = 1
            click_y = Menu.btn_location(menu_start, menu_end, buffer, 7, args[0] - 1)
            GAME.click_input(coords=(100, click_y))

    def __str__(self):
        return "Facilities & Distance Menu\nValid Commands:\nfacilities\ndistance\nplanet <1-7>\nback"


class ShopMenu(BottomButtonMenu):
    right_menu_start = 230
    right_menu_buffer = 30
    right_menu_end = 500
    right_menu_amount = 3
    resources = ["cantaloupe", "jelly beans", "moon ferns", "frog legs", "whip cream", "babel seeds", "diapers",
                 "umbrellas", "toasters", "hair tonic", "polyester", "lava lamps", "oxygen", "oggle sand",
                 "kryptoons", "x fuels", "gems", "exotic"]

    def __init__(self):
        super().__init__(3)
        self.commands = self.commands + ["market", "marketplace", "show", "supply", "warehouse"]

    def click_right_button(self, number):
        ycoord = Menu.btn_location(self.right_menu_start,
                                   self.right_menu_end,
                                   self.right_menu_buffer,
                                   self.right_menu_amount,
                                   number)
        GAME.click_input(coords=(675, ycoord))

    def manage_resource(self, top_button, args):
        if not (args[-1].isdigit() or args[-1] in ["max", "all"]):
            args.append("max")
        if len(args) < 2:
            return
        if len(args) == 3:
            # Combine multi-word resources back into 1 element
            args[0] = args[0] + " " + args[1]
            args[1] = args[2]
        if args[0] in ShopMenu.resources and (args[1].isdigit() or args[1] in ["max", "all"]):
            # If the request is valid
            # open available / cargo menu depending on buy / sell
            if top_button:
                self.click_right_button(2)
            else:
                self.click_right_button(3)
            # Attempt to click on the resource, this will fail if it is already selected as the bold text is
            # not detected. If that happens, click on the "show all" menu to unbold every resource
            try:
                item = locateOnScreen("ui_imgs/marketplace/" + args[0] + ".png")
                click(item)
            except ImageNotFoundException:
                self.click_right_button(4)
                try:
                    item = locateOnScreen("ui_imgs/marketplace/" + args[0] + ".png")
                    click(item)
                except ImageNotFoundException:
                    pass
            # Click the 'action' button and open the money menu
            if top_button:
                self.click_right_button(0)
            else:
                self.click_right_button(1)
            self.money_menu(args[1])
            # This includes a call to close any menus that may have opened due to a failure


class SupplyMenu(ShopMenu):
    def __init__(self):
        super().__init__()
        self.commands.remove("supply")
        self.commands.append("mark")

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if command == "market" or command == "marketplace":
            self.click_button(1)
            self.next_menu = MarketMenu()
        elif command == "warehouse":
            self.click_button(2)
            self.next_menu = WarehouseMenu()
        elif command == "show" and len(args) > 0:
            if args[0] == "available":
                self.click_right_button(0)
            elif args[0] == "cargo":
                self.click_right_button(1)
            elif args[0] == "all":
                self.click_right_button(2)
        elif command == "mark" and len(args) > 0:
            if args[0].isdigit():
                xcoord = Menu.btn_location(220, 550, 20, 6, int(args[0]) - 1)
                GAME.click_input(coords=(xcoord, 100))

    def __str__(self):
        return "Supply Menu\nValid Commands:\nmarket/marketplace\nwarehouse\nshow <available/cargo/all>\nmark " \
               "<1-6>\nback"


class MarketMenu(ShopMenu):
    right_menu_amount = 5

    def __init__(self):
        super().__init__()
        self.commands = self.commands[2:] + ["buy", "sell"]

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if command == "supply":
            self.click_button(1)
            self.next_menu = SupplyMenu()
        elif command == "warehouse":
            self.click_button(2)
            self.next_menu = WarehouseMenu()
        if len(args) > 0:
            if command == "show":
                if args[0] == "available":
                    self.click_right_button(2)
                elif args[0] == "cargo":
                    self.click_right_button(3)
                elif args[0] == "all":
                    self.click_right_button(4)
            elif command == "buy":
                self.manage_resource(True, args)
            elif command == "sell":
                self.manage_resource(False, args)

    def __str__(self):
        return "Marketplace Menu\nValid Commands:\nsupply\nwarehouse\nshow <available/cargo/all>\nbuy <resource> " \
               "<amount/max>\nsell <resource> <amount/max>\nback"


class WarehouseMenu(ShopMenu):
    right_menu_start = 84
    right_menu_end = 530
    right_menu_amount = 6

    def __init__(self):
        super().__init__()
        self.commands.remove("warehouse")
        self.commands = self.commands + ["store", "take", "other"]

    def _execute(self, command, args=[]):
        super()._execute(command, args)
        if command == "supply":
            self.click_button(1)
            self.next_menu = SupplyMenu()
        elif command == "marketplace":
            self.click_button(2)
            self.next_menu = MarketMenu()
        elif command == "other":
            self.click_right_button(5)
            sleep(3)
            Menu.close_pop_up()
        elif len(args) > 0:
            if command == "show":
                if args[0] == "available":
                    self.click_right_button(2)
                elif args[0] == "cargo":
                    self.click_right_button(3)
                elif args[0] == "all":
                    self.click_right_button(4)
            elif command == "store":
                self.manage_resource(True, args)
            elif command == "take":
                self.manage_resource(False, args)

    def __str__(self):
        return "Warehouse Menu\nValid Commands:\nsupply\nmarket/marketplace\nshow <available/cargo/all>\nstore " \
               "<resource> <amount/max>\ntake <resource> <amount/max>\nback"


class AuctionMenu(Menu):

    def __init__(self):
        super().__init__()
        GAME.click_input(coords=(600, 530))  # Click OK to open the auction dialouge box

    def run(self, command):
        print(command,command.isdigit())
        if command.isdigit():
            print("bidding muhaha")
            self._execute(command)
        else:
            super().run(command)

    def _execute(self, command, args=[]):
        print("hi")
        super()._execute(command)
        print(command, command.isdigit())
        if command.isdigit():
            print("Ok now we're actually bidding")
            GAME.click_input(coords=(300, 425)) # Click the text box
            keyboard.send_keys(command)
            keyboard.send_keys("{ENTER}") # Make Bid
            GAME.click_input(coords=(350, 380)) # Click Yes in case the game thinks we're bidding too much

