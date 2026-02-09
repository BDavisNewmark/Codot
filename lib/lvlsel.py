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
    global done
    done = levelnum
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
    global screen, scale, exist, mouse, place, buttons, loaded
    screen = window
    scale = scalar
    exist = 0
    while True:
        try: open(f"./levels/level_{exist}.csv")
        except: break
        else: exist += 1

    mouse = Cursor(point = (1/2, 1), size = mouse_size)

    place = lambda n : ((n % lvlsel_grid[0]) * (lvlsel_size + lvlsel_gap) + (screen.get_width() - lvlsel_size * lvlsel_grid[0] - lvlsel_gap * (lvlsel_grid[0] - 1)) // 2, (n // lvlsel_grid[0]) * (lvlsel_size + lvlsel_gap) + (screen.get_height() - lvlsel_size * lvlsel_grid[1] - lvlsel_gap * (lvlsel_grid[1] - 1)) // 2)
    
    def button(n: int) -> Callable[[Tuple[int, int]], bool]:
        return lambda pos : (pos[0] - place(n)[0] - lvlsel_size / 2) ** 2 + (pos[1] - place(n)[1] - lvlsel_size / 2) ** 2 < (lvlsel_size / 2) ** 2

    buttons = []
    for i in range(exist):
        buttons.append(button(i))
    buttons = tuple(buttons)

    lscreen = pygame.Surface(screen.get_size())
    bg = pygame.image.load("./sprites/level/bgb.png")
    bg = pygame.transform.scale(bg, lscreen.get_size())
    shade = pygame.Surface(lscreen.get_size())
    shade.fill("black")
    shade.set_alpha(69)
    bg.blit(shade, (0, 0))
    lscreen.blit(bg, (0, 0))
    for i in range(exist):
        sprite = pygame.image.load(f"./sprites/player/{'blue' if i <= done else 'red'}_player.png")
        sprite = pygame.transform.scale(sprite, (lvlsel_size, lvlsel_size))
        lscreen.blit(sprite, place(i))
    loaded = lscreen


def run() -> int:
    lscreen = loaded.copy()
    
    hovered = mouse.hover(*buttons)

    pygame.event.get()

    for i in range(exist):
        if i == hovered:
            sprite = pygame.image.load(f"./sprites/player/{'blue' if i <= done else 'red'}_player_hold.png")
            sprite = pygame.transform.scale(sprite, (lvlsel_size, lvlsel_size))
            lscreen.blit(sprite, place(i))

    mice, out = mouse.draw(lscreen.get_size(), *buttons)
    lscreen.blit(mice, (0, 0))

    screen.blit(lscreen, (0, 0))
    return out if out <= done else -1