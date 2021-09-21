from clicker import Clicker
import keyboard as kb
from time import sleep

clicker = Clicker()


def on_toggle(event):
    if clicker.is_clicking():
        clicker.stop()
        return
    clicker.start()


kb.on_release_key('a', on_toggle)

while True:
    sleep(1)
