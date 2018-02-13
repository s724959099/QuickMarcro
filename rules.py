from pynput.keyboard import Key
from pynput.mouse import Button
rules = {
    "stop": Key.f11,
    "exit": Key.f12,
    "rules": [{
        'input': {
            'type': 'keyboard',
            'data': 'q'
        },
        'output': [{
            'type': 'keyboard',
            'data': 'q'
        }, {
            'type': 'keyboard',
            'data': Key.space
        }]
    }, {
        'input': {
            'type': 'scroll',
            'data': 1
        },
        'output': [{
            'type': 'button',
            'data': Button.middle
        }, {
            'type': 'button',
            'data': Button.right
        }]
    }, ]
}
