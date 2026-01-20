import pygame
import level
import draw
import lvlsel



desksize = pygame.display.get_desktop_sizes()[0]
scale = min(1, desksize[0] / 1280, desksize[1] / 720)
screen = pygame.display.set_mode((int(1280 * scale), int(720 * scale)))
pygame.display.set_caption("Codot")
pygame.mouse.set_visible(False)


level.init(screen, scale, 4)
draw.init()
lvlsel.init(screen, scale)

while level.running:
    level.step()
    draw.draw()
    pygame.display.flip()