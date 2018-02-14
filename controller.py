from rules import rules
import ODict
import sys
import time
import threading
from pynput import mouse
from pynput import keyboard

my_mouse = mouse.Controller()
my_keyboard = keyboard.Controller()


class Starter:
    def __init__(self, rules):
        self.stop = self.key_replace(rules.stop)
        self.exit = self.key_replace(rules.exit)
        self.start = self.key_replace(rules.start) if hasattr(rules, 'start') else None
        self.start_status = True

    def key_replace(self, data):
        if isinstance(data, str):
            data = keyboard.KeyCode(char=data)
        return data

    def add(self, *args, **kwargs):
        self.threads = [*args]

    def execute(self, key):
        if key == self.exit:
            print("exit")
            for t in self.threads:
                t.stop()
        if key == self.stop:
            self.start_status = False if self.start else not self.start_status
        if key == self.start:
            self.start_status = True


class KeyController:
    def __init__(self, rule):
        self.rule = rule

    def key_replace(self, data):
        if isinstance(data, str):
            data = keyboard.KeyCode(char=data)
        return data

    def execute(self, key):
        if self.key_replace(self.rule.input.data) == key:
            for item in self.rule.output:
                if item.type == 'keyboard' and self.key_replace(item.data) != key:
                    my_keyboard.press(item.data)
                    my_keyboard.release(item.data)
                if item.type == 'button' and self.key_replace(item.data) != key:
                    my_mouse.press(item.data)
                    my_mouse.release(item.data)


class ScrollController:
    def __init__(self, rule):
        self.rule = rule
        self.in_execute = False
        self.dy = None  # >1 往下 <1 往上

    def thread(self):

        time.sleep(0.5)
        self.in_execute = False

    def start(self):
        t = threading.Thread(target=self.thread)
        t.start()

    def execute(self, dy):
        if dy != 0:
            self.dy = dy
        condi1 = self.rule.input.data > 0 and self.dy > 0
        condi2 = self.rule.input.data < 0 and self.dy < 0
        if not self.in_execute and (condi1 or condi2):
            self.in_execute = True
            self.start()
            print("Start")
            for item in self.rule.output:
                if item.type == 'keyboard':
                    my_keyboard.press(item.data)
                    my_keyboard.release(item.data)
                if item.type == 'button':
                    my_mouse.press(item.data)
                    my_mouse.release(item.data)


def rule_factories(rules):
    scroll_events = []
    key_events = []
    for item in rules:
        if item.input.type == 'keyboard':
            key_events.append(KeyController(item))
        if item.input.type == 'scroll':
            scroll_events.append(ScrollController(item))
    return scroll_events, key_events


rules = ODict(rules)
starter = Starter(rules)
scroll_events, key_events = rule_factories(rules.rules)
