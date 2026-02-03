import pygame
from constants import *
from typing import *
from os import remove
from classes import Cursor
import level

pygame.init()



devmode = False
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
    global dim, screen, scale, exist, mouse, place, buttons
    dim = level.dim
    screen = window
    scale = scalar
    exist = 0
    while True:
        try: open(f"./levels/level_{exist}.csv")
        except: break
        else: exist += 1

    mouse = Cursor(point = (1/2, 1))

    place = lambda n : ((n % lvlsel_grid[0]) * (lvlsel_size + lvlsel_gap) + (screen.get_width() - lvlsel_size * lvlsel_grid[0] - lvlsel_gap * (lvlsel_grid[0] - 1)) // 2, (n // lvlsel_grid[1]) * (lvlsel_size + lvlsel_gap) + (screen.get_height() - lvlsel_size * lvlsel_grid[1] - lvlsel_gap * (lvlsel_grid[1] - 1)) // 2)
    
    def button(n: int) -> Callable[[Tuple[int, int]], bool]:
        return lambda pos : (pos[0] - place(n)[0] - lvlsel_size / 2) ** 2 + (pos[1] - place(n)[1] - lvlsel_size / 2) ** 2 < (lvlsel_size / 2) ** 2

    buttons = []
    for i in range(exist):
        buttons.append(button(i))
    buttons = tuple(buttons)


def run() -> int:
    lscreen = pygame.Surface(screen.get_size())
    bg = pygame.image.load("./sprites/level/bgb.png")
    bg = pygame.transform.scale(bg, lscreen.get_size())
    shade = pygame.Surface(lscreen.get_size())
    shade.fill("white")
    shade.set_alpha(69)
    bg.blit(shade, (0, 0))
    bg.blit(lscreen, (0, 0))
    
    hovered = mouse.hover(scale, *buttons)

    for i in range(exist):
        sprite = pygame.image.load(f"./sprites/player/{'blue' if i <= done else 'red'}_player{'_hold' if i == hovered else ''}.png")
        sprite = pygame.transform.scale(sprite, (lvlsel_size, lvlsel_size))
        sprite.blit(lscreen, place(i))

    lscreen.blit(screen, (0, 0))
    mice = mouse.draw(lscreen.get_size(), scale, *buttons)
    mice.blit(lscreen, (0, 0))
    
    return 0