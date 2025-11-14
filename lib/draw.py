import pygame
import pymunk
from pymunk import pygame_util
import level


screen = level.screen
space = level.space

scalef = lambda x1, y1, x2, y2 : max(x1 / x2, y1 / y2)

def draw() -> pygame.Surface:
    bg = pygame.image.load("./sprites/level/bg.png")
    bg = pygame.transform.scale_by(bg, scalef(*screen.get_size(), *bg.get_size()))
    screen.blit(bg, (0, 0))

    ground = pymunk.Space()
    groundv = pygame_util.DrawOptions(screen)
    body = space.static_body.copy()
    groundv.shape_outline_color = (0, 0, 0, 0)
    groundv.shape_static_color = (0, 0, 0, 255)
    ground.add(body)
    ground.debug_draw(groundv)
    