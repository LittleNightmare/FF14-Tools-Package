# from playsound import playsound
import time
from threading import Thread

from pygame import mixer


def play_(name):
    mixer.init()
    mixer.music.load(name)
    mixer.music.play()
    time.sleep(2)


def play_mp3(name):
    Thread(target=play_, args=(name,)).start()


if __name__ == '__main__':
    play_mp3('start.mp3')
