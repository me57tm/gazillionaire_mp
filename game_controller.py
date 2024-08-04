from pywinauto import Application, keyboard

app = Application().connect(path='Gazillionaire.exe')
GAME = app.Gazillionaire
GAME.move_window(x=None, y=None, width=800, height=627)

class Menu:
    global GAME
    commands = []
    next_menu = None

    def process_command(self, command):
        command_parts = command.split(" ")
        command = command_parts[0]
        if command in self.commands:
            if len(command_parts > 1):
                args = command_parts[1:]
            self.execute(command, args)

    def execute(self, command, args):
        pass

    def moneyMenu(self,amount):
        #stocks upper not the same
        if amount == "max":
            GAME.click_input(coords=(460, 370))
        else:
            try:
                int(amount)
                keyboard.send_keys(amount)
            except ValueError:
                pass
        GAME.click_input(coords=(400, 435))

    def __str__(self):
        return self.commands

class MainMenu(Menu):
    commands = [
        "marketplace","market", "supply","warehouse"
        "passengers",
        "pick",
        "passenger",
        "advertise",
        "ad",
        "advert",
        "pay",
        "buy",
        "explore",
        "stocks",
        "stock,"
        "bank",
        "loan",
        "zinn",
        "zinns",
        "journey",
        "travel",
        "leave",
    ]
    def execute(self, command, args):
        match command:
            case "marketplace" | "market":
                GAME.click_input(coords=(350, 150))
            case "supply":
                pass
            case "warehouse":
                pass
            case "journey" | "travel" | "leave":
                GAME.click_input(coords=(150, 150))
            case "stock" | "stocks":
                GAME.click_input(coords=(200, 350))
            # case "money:
                # game.click_input(coords=(200, 400))
            case "bank":
                GAME.click_input(coords=(200, 450))
            case "loan":
                GAME.click_input(coords=(200, 500))
            case "zinn" | "zinns":
                GAME.click_input(coords=(200, 550))
            case "pick" | "passenger" | "passengers":
                GAME.click_input(coords=(500, 250))
            case "advert" | "advertise" | "ad":
                GAME.click_input(coords=(500, 300))
            case "pay":
                GAME.click_input(coords=(200, 350))
                GAME.click_input(coords=(200, 400))
            case "buy":
                GAME.click_input(coords=(200, 450))
            case "explore":
                GAME.click_input(coords=(200, 500))
