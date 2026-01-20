import pygame
import pymunk
from pymunk import pygame_util
import map
import level
from constants import *
from math import *


dev_mode = False
sticky_ground_type = True



def init():
    global screen, space, scale, dim, gp, levelnum, lscreen, draw_options, player1, player2, new
    screen = level.screen
    space = level.space
    scale = level.scale
    dim = level.dim
    gp = level.gp
    levelnum = level.levelnum
    lscreen = pygame.Surface(dim)
    draw_options = level.draw_options
    player1 = level.player1
    player2 = level.player2
    new = nax
    

scalef = lambda x1, y1, x2, y2 : min(x1 / x2, y1 / y2)



loaded = []
new = nax

def draw():
    global lscreen, new, loaded, cover
    if dev_mode:
        lscreen.fill("white")
        gspace = pymunk.Space()
        hbody = pymunk.Body(body_type = pymunk.Body.STATIC)
        gspace.add(hbody)
        if new:
            ground = map.load(levelnum, gspace, hbody, not sticky_ground_type, sticky_ground_type)
            loaded.append(ground)
        else:
            ground = loaded[0]
        dog = pygame_util.DrawOptions(lscreen)
        gspace.debug_draw(dog)
        lscreen = pygame.transform.scale_by(lscreen, scalef(*screen.get_size(), *dim))
        screen.blit(lscreen, (0, 0))
        pygame.display.flip()
        new -= 1
        
    else:
        lscreen = pygame.Surface(dim)
        lscreen.fill(behind)
        screen.fill(behind)

        if new == nax:
            bg = pygame.image.load("./sprites/level/bgb.png")
            bg = pygame.transform.scale(bg, lscreen.get_size())
            shade = pygame.Surface(lscreen.get_size())
            shade.fill("white")
            shade.set_alpha(69)
            bg.blit(shade, (0, 0))
            loaded.append(bg)
        else:
            bg = loaded[0]
        lscreen.blit(bg, (0, 0))
        
        if new == nax:
            try: img1 = pygame.image.load(f"./sprites/maps/level_{levelnum}/normal.png")
            except:
                img1 = pygame.Surface((1, 1))
                img1.fill("white")
            img1.set_colorkey("white")
            loaded.append(img1)
        else:
            img1 = loaded[1]
        lscreen.blit(img1, (0, 0))
        
        if new == nax:
            try: img2 = pygame.image.load(f"./sprites/maps/level_{levelnum}/sticky.png")
            except:
                img2 = pygame.Surface((1, 1))
                img2.fill("white")
            img2.set_colorkey("white")
            loaded.append(img2)
        else:
            img2 = loaded[2]
        lscreen.blit(img2, (0, 0))

        if new == nax:
            texts = pygame.Surface(lscreen.get_size())
            texts.fill("white")
            texts.set_colorkey("white")
            m = map.load(levelnum, space, level.hbody, False, False, True)
            if len(m) > 4:
                for x in m[4:]:
                    texts.blit(x[0], (x[1], x[2]))
            loaded.append(texts)
        else:
            texts = loaded[3]
        lscreen.blit(texts, (0, 0))
                
        if new == nax:
            goal = pygame.image.load("./sprites/level/flag.png")
            goal = pygame.transform.scale(goal, (flag_size, flag_size))
            loaded.append(goal)
        else:
            goal = loaded[4]
        lscreen.blit(goal, (gp[0] - goal.get_width() / 2, gp[1] - goal.get_height()))

        if new == nax:
            girth = player1.shape.radius * rod_girth
            loaded.append(girth)
            rod = pygame.image.load("./sprites/player/rod.png")
            loaded.append(rod)

            
        else:
            girth = loaded[5]
            rod = loaded[6]
            rod = pygame.transform.scale(rod, (player1 + player2, girth))
            rod = pygame.transform.rotate(rod, -degrees(player1 - player2))
        lscreen.blit(rod, ((player1.body.position[0] + player2.body.position[0] - rod.get_width()) / 2, (player1.body.position[1] + player2.body.position[1] - rod.get_height()) / 2))
        
        sprite1 = level.player1.spriter(player2 - player1)
        lscreen.blit(sprite1, (player1.body.position[0] - sprite1.get_width() / 2, player1.body.position[1] - sprite1.get_height() / 2))
        
        sprite2 = level.player2.spriter(player1 - player2)
        lscreen.blit(sprite2, (player2.body.position[0] - sprite2.get_width() / 2, player2.body.position[1] - sprite2.get_height() / 2))
        

        if new == nax:
            cover = pygame.Surface(lscreen.get_size())
            cover.fill("black")
        if new > 0:
            cover.set_alpha(int(255 * new / nax)) # type: ignore
            lscreen.blit(cover, (0, 0)) # type: ignore
        
        lscreen = pygame.transform.scale_by(lscreen, scalef(*screen.get_size(), *dim))
        screen.blit(lscreen, ((screen.get_width() - lscreen.get_width()) / 2, (screen.get_height() - lscreen.get_height()) / 2))
        pygame.display.flip()
        new -= 1

    
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