from pynput import keyboard
from pynput import mouse
from controller import starter, scroll_events, key_events


def on_press(key):
    starter.execute(key)
    if starter.start_status:
        for item in key_events:
            item.execute(key)


def on_release(key):
    pass


def on_scroll(x, y, dx, dy):
    if starter.start_status:
        for item in scroll_events:
            item.execute(dy)


def main():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        with mouse.Listener(
                on_scroll=on_scroll) as mouse_listener:
            starter.add(listener, mouse_listener)
            listener.join()
            mouse_listener.join()


if __name__ == '__main__':
    main()
