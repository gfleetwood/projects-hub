# Uses pyinput to use the keyboard as a mouse

from pynput import keyboard
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener, KeyCode

def on_activate_up():

    def on_press(key):
        mouse.move(0, -5)

    def on_release(key):
        if key == KeyCode(char = "w"):
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def on_activate_click_left():
    mouse.click(Button.left)

"""
All the other global hot key callback functions would be here.
"""

mouse = Controller()
  
with keyboard.GlobalHotKeys({
        'p+w': on_activate_up,
        'p+d': on_activate_right,
        'p+s': on_activate_down,
        'p+a': on_activate_left,
        'p+q': on_activate_click_left,
        'p+e': on_activate_click_right}) as h:
    h.join()
