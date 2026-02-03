import pymunk
from constants import *
import csv
from math import *
from typing import *
import pygame


def load(level: int, space: pymunk.Space, sticky: pymunk.Body, icy: pymunk.Body, g: bool = True, h: bool = True, s: bool = True, t: bool = False) -> List[Tuple[int, int] | Tuple[pygame.surface.Surface, float, float]]:
    output = []
    with open(f"./levels/level_{level}.csv") as c:
        reader = csv.reader(c)
        for i, row in enumerate(reader):
            fric = True
            if i == 0: output = [(float(row[0]), float(row[1])), (float(row[2]), float(row[3])), (float(row[4]), float(row[5])), (float(row[6]), float(row[7]))]
            else:
                if "g" in row[0]:
                    if g: b = space.static_body
                    else: continue
                elif "h" in row[0]:
                    if h: b = sticky
                    else: continue
                elif "i" in row[0]
                    if s: b = icy; fric = False
                    else: continue
                if "l" in row[0]:
                    x = pymunk.Segment(b, (float(row[1]), float(row[2])), (float(row[3]), float(row[4])), float(row[5]) / 2) # type: ignore
                    x.friction = floor_friction if fric else ice_friction
                    space.add(x)                
                elif "p" in row[0]:
                    points = []
                    for i in range(1, len(row), 2): points.append((float(row[i]), float(row[i + 1])))
                    x = pymunk.Poly(b, points) # type: ignore
                    x.friction = floor_friction if fric else ice_friction
                    space.add(x)
                elif "a" in row[0]:
                    xc, yc, inr, outr, start, end = float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6])
                    points = []
                    for i in range(circle_sides):
                        angle = radians(start + i * (end - start) / circle_sides)
                        points.append((xc + outr * cos(angle), yc + outr * sin(angle)))
                    for i in range(circle_sides):
                        angle = radians(end - (i + 1) * (end - start) / circle_sides)
                        points.append((xc + inr * cos(angle), yc + inr * sin(angle)))
                    x = pymunk.Poly(b, points) # type: ignore
                    x.friction = floor_friction if fric else ice_friction
                    space.add(x)
                elif row[0] == "t" and t:
                    x = font.render(row[4], False, fcolor)
                    x = pygame.transform.scale_by(x, fscale * float(row[3]))
                    output.append((x, float(row[1]), float(row[2])))
    return output # type: ignore