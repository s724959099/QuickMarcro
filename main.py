from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
import sys
from rules import rules
import ODict
import pdir
from pynput.mouse import Button
import threading

rules = ODict(rules)
my_mouse = mouse.Controller()
my_keyboard = keyboard.Controller()
execute_status = True


def key_replace(data, key):
    if isinstance(data, str):
        key = str(key).replace("'", "")
    return key


def execute_output(arr, prevent_data):
    for item in arr:
        if item.type == 'keyboard' and item.data != prevent_data:
            my_keyboard.press(item.data)
            my_keyboard.release(item.data)
        if item.type == 'button' and item.data != prevent_data:
            my_mouse.press(item.data)
            my_mouse.release(item.data)


def on_press(key):
    data = key_replace(rules.stop, key)
    if rules.stop == data:
        execute_status != execute_status
    if not execute_status:
        return
    for item in rules.rules:
        if item.input.type == 'keyboard':
            data = key_replace(item.input.data, key)
            if data == item.input.data:
                execute_output(item.output, item.input.data)
    return True


def on_release(key):
    key = key_replace(rules.exit, key)
    if key == rules.exit:
        sys.exit()
    return True


def on_scroll(x, y, dx, dy):
    for item in rules.rules:
        if item.input.type == 'scroll':
            data = dy
            if data == item.input.data:
                execute_output(item.output, item.input.data)
    return True


def main():
    while True:
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            with mouse.Listener(
                    on_scroll=on_scroll) as mouse_listener:
                listener.join()
                mouse_listener.join()


if __name__ == '__main__':
    main()
