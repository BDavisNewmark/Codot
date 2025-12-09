import pygame
from pygame.transform import average_color
import pymunk
from pymunk import pygame_util
import map
import level


dev_mode = True
sticky_ground_type = False



def init():
    global screen, space, scale, dim, gp, levelnum, lscreen, draw_options
    screen = level.screen
    space = level.space
    scale = level.scale
    dim = level.dim
    gp = level.gp
    levelnum = level.levelnum
    lscreen = pygame.Surface(dim)
    draw_options = level.draw_options
    

scalef = lambda x1, y1, x2, y2 : min(x1 / x2, y1 / y2)


def draw():
    global lscreen
    if dev_mode:
        lscreen.fill("white")
        gspace = pymunk.Space()
        hbody = pymunk.Body(body_type = pymunk.Body.STATIC)
        gspace.add(hbody)
        ground = map.load(levelnum, gspace, hbody, not sticky_ground_type, sticky_ground_type)
        dog = pygame_util.DrawOptions(lscreen)
        gspace.debug_draw(dog)
        lscreen = pygame.transform.scale_by(lscreen, scalef(*screen.get_size(), *dim))
        screen.blit(lscreen, (0, 0))
        pygame.display.flip()
        
    else:
        bg = pygame.image.load("./sprites/level/bg.png")
        bg = pygame.transform.scale_by(bg, scale)
        screen.blit(bg, (0, 0))
        img1 = pygame.image.load(f"./sprites/maps/level_{levelnum}/normal.png")
        img1 = pygame.transform.scale_by(img1, scale)
        img2 = pygame.image.load(f"./sprites/maps/level_{levelnum}/sticky.png")
        img2 = pygame.transform.scale_by(img2, scale)
        screen.blit(img1, (0, 0))
        screen.blit(img2, (0, 0))

    
    """mask = pygame.Surface(lscreen.get_size())
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
    back.blit(mask, (0, 0), special_flags = pygame.BLEND_RGB_SUB)
    fore = average_color(mask)
    back.set_colorkey(fore)
    gsprite.blit(back, (0, 0), special_flags = pygame.BLEND_RGB_SUB)
    gsprite.set_colorkey("black")
    lscreen.blit(gsprite, (0, 0), special_flags = pygame.BLEND_RGB_SUB)

    hmask = pygame.Surface(lscreen.get_size())
    hground = pymunk.Space()
    hgroundv = pygame_util.DrawOptions(hmask)
    hgbody = pymunk.Body(body_type = pymunk.Body.STATIC)
    hground.add(hgbody)
    map.load(levelnum, hground, hgbody, False, True)
    hgsprite = pygame.image.load("./sprites/level/hground.png")
    hgsprite = pygame.transform.scale_by(hgsprite, scalef(*lscreen.get_size(), *hgsprite.get_size()))
    hground.debug_draw(hgroundv)
    hmask.blit(lscreen, (0, 0))
    hback = pygame.Surface(lscreen.get_size())
    hback.fill("black")
    hback.blit(hmask, (0, 0), special_flags = pygame.BLEND_RGB_SUB)
    hfore = average_color(hmask)
    hback.set_colorkey(hfore)
    hgsprite.blit(hback, (0, 0), special_flags = pygame.BLEND_RGB_SUB)
    hgsprite.set_colorkey("black")
    lscreen.blit(hgsprite, (0, 0), special_flags = pygame.BLEND_RGB_SUB)

    lscreen = pygame.transform.scale_by(lscreen, scalef(*screen.get_size(), *lscreen.get_size()))
    screen.blit(lscreen, (0, 0))"""