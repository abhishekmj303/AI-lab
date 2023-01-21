import time
import threading, _thread
from pynput.keyboard import Key, Controller, Listener, HotKey

# Complete path to the code
file_path = "/home/abhishek/Programs/AI/lab02/two-jug.py"

# "\t" if indented using tab
indent_string = "    "

# Delay to start typing the code in seconds
initial_delay = 5

# Delay between each letter while typing in seconds
key_delay = 0.01

# Note: Kill the program from typing the code by pressing <alt>+c
# Kill Switch
switch = '<alt>+c'

# TODO : fix indentation when 'break', 'continue' or 'return' keywords

def type_code():
    keyboard = Controller()
    with open(file_path, "r") as f:
        codelines = f.readlines()
        indent_count = 0
        for code in codelines:
            curr_indent = code.count(indent_string)
            if curr_indent < indent_count:
                for _ in range(indent_count - curr_indent):
                    keyboard.press(Key.backspace)
                    keyboard.release(Key.backspace)
                    time.sleep(key_delay)
                indent_count = curr_indent
            elif curr_indent > indent_count:
                for _ in range(curr_indent - indent_count):
                    keyboard.press(Key.tab)
                    keyboard.release(Key.tab)
                    time.sleep(key_delay)
                indent_count = curr_indent
            
            code = code.replace(indent_string, "")
            for a in code:
                keyboard.type(a)
                time.sleep(key_delay)

            if code[-2:] in [":\n", "[\n", "(\n", "{\n"]:
                indent_count += 1

        time.sleep(0.5)
        keyboard.press(Key.home)
        keyboard.release(Key.home)
        keyboard.press(Key.shift)
        keyboard.press(Key.end)
        keyboard.release(Key.end)
        keyboard.release(Key.shift)
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)


def kill_switch():

    def on_activate():
        _thread.interrupt_main()
        exit()

    def for_canonical(f):
        return lambda k: f(l.canonical(k))

    hotkey = HotKey(HotKey.parse(switch), on_activate)
    with Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)) as l:
        l.join()


if __name__ == "__main__":
    threading.Thread(target=kill_switch, daemon=True).start()
    time.sleep(initial_delay)
    type_code()
