import pygame
from pygame.transform import average_color
import pymunk
from pymunk import pygame_util
import map
import level


def init():
    global screen, space, scale, dim, gp, levelnum, lscreen
    screen = level.screen
    space = level.space
    scale = level.scale
    dim = level.dim
    gp = level.gp
    levelnum = level.levelnum
    lscreen = pygame.Surface(dim)
    

scalef = lambda x1, y1, x2, y2 : max(x1 / x2, y1 / y2)

def draw() -> pygame.Surface:
    bg = pygame.image.load("./sprites/level/bg.png")
    bg = pygame.transform.scale_by(bg, scalef(*screen.get_size(), *bg.get_size()))
    screen.blit(bg, (0, 0))

    mask = pygame.Surface(lscreen.get_size())
    ground = pymunk.Space()
    groundv = pygame_util.DrawOptions(mask)
    gbody = pymunk.Body(body_type = pymunk.Body.STATIC)
    ground.add(gbody)
    map.load(levelnum, ground, gbody, True, False)
    gsprite = pygame.image.load("./sprites/level/ground.png")
    gsprite = pygame.transform.scale_by(gsprite, scalef(*lscreen.get_size(), *gsprite.get_size()))
    ground.debug_draw(groundv)
    mask.blit(lscreen, (0, 0))
    back = pygame.Surface(lscreen.get_size())
    back.fill("black")
    back.blit(mask, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)
    fore = average_color(mask)
    back.set_colorkey(fore)
    gsprite.blit(back, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)
    gsprite.set_colorkey("black")
    screen.blit(gsprite, (0, 0))