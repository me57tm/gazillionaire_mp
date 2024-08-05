# This is a sample Python script.
import pyautogui


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

#location = pyautogui.locateOnScreen('buttons/x.png')
#pyautogui.click(location)

'''import pywinauto

app = pywinauto.Application().connect(path='Gazillionaire.exe')
game = app.Gazillionaire
game.move_window(x=None, y=None, width=776, height=609)
#Game window (Inc. Title Bar) - 760 * 600
#Game window (Exc. Title Bar) - 760 * 570

x = ""
while x != "quit":
    x = input(">>>")
    if x == "ss":
        game.capture_as_image().save('screenshot.png')
    elif x == "x":
        try:
            location = pyautogui.locateOnScreen('x.png')
            pyautogui.click(location)
        except pyautogui.ImageNotFoundException:
            pass
    else:
        x = x.split(" ")
        x[0] = int(x[0])
        x[1] = int(x[1])
        game.click_input(coords=(x[0], x[1]))'''

from game_controller import *

controller = MainMenu()
controller.execute("travel")

x = 0
while x != "quit":
    x = input(">>>")
    if len(x) > 5 and x[:5] == "click":
        x = x.split(" ")
        x[1] = int(x[1])
        x[2] = int(x[2])
        GAME.click_input(coords=(x[1], x[2]))
    else:
        controller.process_command(x)
    controller = controller.next_menu