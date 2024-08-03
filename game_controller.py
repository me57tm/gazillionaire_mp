class Menu:
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

    def __str__(self):
        return self.commands

class MainMenu(Menu):
    commands = [
        "marketplace", "supply","warehouse"
        "passengers",
        "advertise",
        "pay",
        "buy",
        "explore",
        "stocks",
        "bank",
        "loan",
        "zinn",
        "journey",
        "travel",
        "leave",
    ]