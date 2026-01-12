import pygame
import level
import draw



desksize = pygame.display.get_desktop_sizes()[0]
scale = min(1, desksize[0] / 1280, desksize[1] / 720)
screen = pygame.display.set_mode((int(1280 * scale), int(720 * scale)))
pygame.display.set_caption("Codot")


level.init(screen, scale, 3)
draw.init()

while level.running:
    level.step()
    draw.draw()
    pygame.display.flip()