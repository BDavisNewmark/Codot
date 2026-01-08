import pygame
from constants import *
from typing import *

pygame.init()


def save(levelnum: int) -> int:
    with open("./save.txt", "r") as file:
        ...

def load() -> int:
    ...