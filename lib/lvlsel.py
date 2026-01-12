import pygame
from constants import *
from typing import *
from os import remove
from classes import Cursor

pygame.init()



done = 0


def save(levelnum: int = done) -> int:
    with open("./save.txt", "w") as file:
        file.write(str(levelnum))
    return levelnum


def load() -> int:
    global done
    try:
        with open("./save.txt", "r") as file:
            done = int(file.read())
    except FileNotFoundError:
        done = 0
    return done


def restart() -> None:
    global done
    remove("./save.txt")
    done = 0


def init(window: pygame.Surface, scalar: float):
    global screen, scale
    screen = window
    scale = scalar