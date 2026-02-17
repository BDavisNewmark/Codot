import pygame
import level
import draw
import lvlsel
from constants import *
from time import sleep



desksize = pygame.display.get_desktop_sizes()[0]
scale = min(1, desksize[0] / 1280, desksize[1] / 720)
screen = pygame.display.set_mode((int(1280 * scale), int(720 * scale)))
pygame.display.set_caption("Codot")
pygame.display.set_icon(pygame.image.load("./sprites/player/blue_player_hold.png"))
pygame.mouse.set_visible(False)


mode = 2
first = True
ran = 0
new = nax
old = pygame.Surface(screen.get_size())
cover = pygame.Surface(screen.get_size())
cover.fill("black")

lvlsel.load()

while True:
    if mode == 0:
        if first:
            level.init(screen, scale, ran)
            draw.init()
            first = False
        if level.step():
            mode = 1
            first = True
            lvlsel.save(lvlsel.done + 1)
        draw.draw()
        pygame.display.flip()

    elif mode == 1:
        if first:
            new = 0
            first = False
            old = pygame.display.get_surface().copy()
        elif new == nax:
            mode = 2
            first = True
            continue
        else:
            new += 1
        out = old.copy()
        ontop = cover.copy()
        ontop.set_alpha(int(255 * new / nax))
        out.blit(ontop, (0, 0))
        screen.blit(out, (0, 0))
        pygame.display.flip()
        sleep(fade_frame)
    
    elif mode == 2:
        if first:
            lvlsel.init(screen, scale)
            first = False
        ran = lvlsel.run()
        pygame.display.flip()
        if ran != -1:
            mode = 0
            first = True
            lvl = ran        