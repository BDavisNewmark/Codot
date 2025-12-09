import pygame
import level
import draw
import datetime
from time import sleep


if datetime.datetime.now().month == 4 and datetime.datetime.now().day == 1:
    desksize = pygame.display.get_desktop_sizes()[0]
    scale = min(1, desksize[0] / 1280, desksize[1] / 720)
    screen = pygame.display.set_mode((int(1280 * scale), int(720 * scale)))
    pygame.display.set_caption("Codot - April Fools!")
    screen.fill("white")
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 100)
    text = font.render("April Fools!", True, "black")
    screen.blit(text, (0, 0))
    pygame.display.flip()
    sleep(10)
    pygame.quit()
    exit()


level.init(2)
draw.init()

while level.running:
    level.step()
    draw.draw()
    pygame.display.flip()