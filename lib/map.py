import pymunk
from constants import *
import csv
from math import *
from typing import *


def load(level: int, space: pymunk.Space, sticky: pymunk.Body, g: bool = True, h: bool = True) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    output = []
    with open(f"../levels/level_{level}.csv") as c:
        reader = csv.reader(c)
        for i, row in enumerate(reader):
            if i == 0:
                output.append((row[0], row[1]))
                output.append((row[2], row[3]))
                output.append((row[4], row[5]))
                output.append((row[6], row[7]))
            else:
                if "g" in row[0]:
                    if g: b = space.static_body
                    else: continue
                elif "h" in row[0]:
                    if h: b = sticky
                    else: continue
                if "l" in row[0]:
                    space.add(pymunk.Segment(b, (float(row[1]), float(row[2])), (float(row[3]), float(row[4])), float(row[5]) / 2)) # type: ignore
                elif "p" in row[0]:
                    points = []
                    for i in range(1, len(row), 2):
                        points.append((float(row[i]), float(row[i + 1])))
                    space.add(pymunk.Poly(b, points)) # type: ignore
                elif "a" in row[0]:
                    points = []
                    for i in range(circle_sides):
                        angle = radians(float(row[5])) + i * (float(row[6]) - float(row[5])) / circle_sides
                        points.append((float(row[1]) + float(row[3]) * cos(angle), float(row[2]) + float(row[3]) * sin(angle)))
                    for i in range(circle_sides):
                        angle = radians(float(row[5])) + (circle_sides - i - 1) * (float(row[6]) - float(row[5])) / circle_sides
                        points.append((float(row[1]) + float(row[4]) * cos(angle), float(row[2]) + float(row[4]) * sin(angle)))
                    space.add(pymunk.Poly(b, points))
    return output # type: ignore