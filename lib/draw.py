import pygame
import pymunk
import level


screen = level.screen
space = level.space

scalef = lambda x1, y1, x2, y2 : max(x1 / x2, y1 / y2)

def draw() -> pygame.Surface:
    bg = pygame.image.load("./sprites/level/bg.png")
    bg = pygame.transform.scale_by(bg, scalef(*screen.get_size(), *bg.get_size()))
    screen.blit(bg, (0, 0))

    ground = pymunk.Space()
    groundv = pymunk.pygame_util.DrawOptions(screen)
    body = space.static_body.copy()
    for x in body.shapes:
        groundv.color_for_shape(x, pygame.Color("black"))
    ground.add(body)
    ground.debug_draw(groundv)
    