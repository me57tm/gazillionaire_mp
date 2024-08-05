from pywinauto import Application, keyboard
from pyautogui import locateOnScreen, click
from time import time, sleep

app = Application().connect(path='Gazillionaire.exe')
GAME = app.Gazillionaire.wait('ready')
GAME.move_window(x=None, y=None, width=776, height=609)


class Menu:
    global GAME
    commands = ["x", "close", "screenshot"]
    next_menu = None

    def __init__(self):
        self.next_menu = self

    def process_command(self, command):
        command_parts = command.split(" ")
        command = command_parts[0]
        args = []
        if command in self.commands:
            if len(command_parts) > 1:
                args = command_parts[1:]
            self.execute(command, args)

    def execute(self, command, args=[]):
        print(command, "args:", args)
        if command == "x" or command == "close":
            self.close_pop_up()
        elif command == "screenshot":
            GAME.capture_as_image().save('screenshots/Gazillionaire' + str(int(time())) + '.png')

    def close_pop_up(self):
        try:
            xbuttoncoords = locateOnScreen('ui_imgs/x.png')
            click(xbuttoncoords)
            success = True
        except:
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

    def execute(self, command, args=[]):
        super().execute(command, args)
        match command:
            case "marketplace" | "market":
                GAME.click_input(coords=(350, 150))
                self.next_menu = BottomButtonMenu(3)
            case "supply":
                GAME.click_input(coords=(500, 150))
            case "warehouse":
                GAME.click_input(coords=(600, 150))
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
                        crew_menu.execute("right")
                        self.close_pop_up()
                        crew_menu.execute("left")
                    elif args[0] == "tax" or args[0] == "taxes":
                        GAME.click_input(coords=(500, 400))
                        GAME.click_input(coords=(450, 530))
                        self.close_pop_up()
                        GAME.click_input(coords=(250, 530))
            case "buy":
                if len(args) > 0:
                    if args[0] == "insurance":
                        GAME.click_input(coords=(500, 450))
                        insurance_menu = TwoButtonEventMenu()
                        insurance_menu.execute("right")
                        self.close_pop_up()
                        insurance_menu.execute("left")
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


class TwoButtonEventMenu(Menu):
    def __init__(self):
        super().__init__()
        self.commands = self.commands + [
            "yes", "left",
            "no", "right"
        ]

    def execute(self, command, args=[]):
        super().execute(command, args)
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

    def execute(self, command, args=[]):
        super().execute(command, args)
        if command == "back":
            self.click_button(0)
            self.next_menu = MainMenu()

    def click_button(self, number):
        buttons_start = 24
        buttons_end = 696
        buttons_width = buttons_end - buttons_start
        spacer = 50
        GAME.click_input(coords=(buttons_start + spacer + number * (buttons_width // self.num_buttons), self.ycoord))


class BankMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(5)
        self.commands = self.commands + ["deposit", "withdraw"]

    def execute(self, command, args=[]):
        super().execute(command, args)
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


class LoanMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(5)
        self.commands = self.commands + ["pay", "borrow"]

    def execute(self, command, args=[]):
        super().execute(command, args)
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


class ZinnMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(3)
        self.commands = self.commands + ["pay"]

    def execute(self, command, args=[]):
        super().execute(command, args)
        if len(args) > 0:
            if command == "pay":
                if args[0] == "back" and len(args) > 1:
                    args[0] = args[1]
                if args[0] == "max":
                    self.click_button(2)
                else:
                    self.click_button(1)
                    self.money_menu(args[0])


class StocksMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(6)
        self.commands = self.commands + ["buy", "sell", "show"]

    def execute(self, command, args=[]):
        super().execute(command, args)
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


class PassengerMenu(BottomButtonMenu):
    ycoord = 550

    def __init__(self):
        super().__init__(3)
        self.commands = self.commands + ["set"]

    def execute(self, command, args=[]):
        super().execute(command, args)
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


class AdvertMenu(TwoButtonEventMenu):
    def __init__(self):
        super().__init__()
        self.commands = self.commands + ["passenger", "commodity", "back"]

    def execute(self, command, args=[]):
        super().execute(command)
        if command == "back":
            self.execute("left")
            self.next_menu = MainMenu()
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
            self.execute("right")


class ExploreMenu(BottomButtonMenu):
    def __init__(self):
        super().__init__(6)
        self.commands = self.commands + ["special", "weather", "news"]

    def execute(self, command, args=[]):

        super().execute(command, args)
        if command == "special":
            self.click_button(1)
            if not self.close_pop_up():
                self.next_menu = SpecialMenu()
        elif command == "weather":
            self.click_button(2)
            sleep(5)
            TwoButtonEventMenu().execute("left")
        elif command == "news":
            self.click_button(3)
            sleep(5)
            TwoButtonEventMenu().execute("left")


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
            print("Tilo!")
            self.tilo = True
            self.commands.remove("special")
            self.commands = self.commands + ["gamble"]
        except:
            self.tilo = False

    def execute(self, command, args=[]):
        print(self.commands)
        super().execute(command, args)
        if self.gambling:
            print("gambling")
            if command == "yes":
                GAME.click_input(coords=(350, 420))
            elif command == "no":
                GAME.click_input(coords=(430, 430))

            try:
                locateOnScreen('ui_imgs/x.png')
            except:
                sleep(1)
                self.next_menu = ExploreMenu()
                self.gambling = False
                self.execute("left")
        else:
            if command == "back":
                self.execute("left")
                self.next_menu = ExploreMenu()
            elif command == "special":
                self.execute("right")
                sleep(4)
                self.next_menu = ExploreMenu()
                self.execute("left")
            elif len(args) > 0 and command == "gamble":
                self.execute("right")
                self.money_menu(args[0])
                try:
                    locateOnScreen('ui_imgs/x.png')
                    self.gambling = True
                    self.commands.remove("gamble")
                    self.commands.remove("back")
                    self.commands = self.commands + ["yes","no"]
                except:
                    sleep(3)
                    self.next_menu = ExploreMenu()
                    self.execute("left")

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

class TravelMenu(BottomButtonMenu):
    PLANETS = []
    def __init__(self):
        super().__init__(3)
        if TravelMenu.PLANETS == []:
            print("Finding planets...")
            i = 0
            for planet in ["bass", "frac", "hork", "loro", "mira", "nosh", "ooom", "pyke", "queg", "stye", "tilo", "vexx", "xeen", "zile"]:
                if i == 7:
                    break
                try:
                    locateOnScreen('ui_imgs/planets/'+ planet + '.png')
                    TravelMenu.PLANETS.append(planet)
                    i += 1
                except:
                    pass
        if len(TravelMenu.PLANETS) != 7:
            print("FAILURE HOW COULD THIS BE")
            print(TravelMenu.PLANETS)
        self.commands = self.commands + ["distance", "facilities"] + TravelMenu.PLANETS

    def execute(self, command, args=[]):
        super().execute(command)
        if command == "distance":
            pass
        elif command == "facilities":
            pass
        elif command in TravelMenu.PLANETS:
            planet_location = locateOnScreen('ui_imgs/planets/' + command + '.png')
            click(planet_location)