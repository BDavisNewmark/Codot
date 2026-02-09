import pygame
import level
import draw
import lvlsel



desksize = pygame.display.get_desktop_sizes()[0]
scale = min(1, desksize[0] / 1280, desksize[1] / 720)
screen = pygame.display.set_mode((int(1280 * scale), int(720 * scale)))
pygame.display.set_caption("Codot")
#pygame.mouse.set_visible(False)


mode = 1
first = True
ran = 0

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
            lvlsel.init(screen, scale)
            first = False
        ran = lvlsel.run()
        pygame.display.flip()
        if ran != -1:
            mode = 0
            first = True
            lvl = ran