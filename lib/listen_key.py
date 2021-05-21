from threading import Thread

from pynput import keyboard


def start_listen(on_press):
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()


def thread_listen(on_press):
    Thread(target=start_listen, args=(on_press,)).start()
