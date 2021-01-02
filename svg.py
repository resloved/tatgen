import svgwrite
import numpy as np
from random import randrange

# -- https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) <= (B[1] - A[1]) * (C[0]-A[0])

def intersect(A, B, C, D):
    if (A == D) or (A == C) or (B == C) or (B == D):
        return False
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
# --

def clear_line(path, verts):
    for i in range(1, len(verts)):
        if intersect(verts[i - 1], verts[i], path[0], path[1]):
            return False
    return True

# -- https://stackoverflow.com/a/35134034
def angle(A, B, C):
    v0 = np.array(A) - np.array(B)
    v1 = np.array(C) - np.array(B)
    return np.degrees(np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1)))
# --

def distance(A, B):
    return abs(A[0] - B[0]) + abs(A[1] - B[1])

def between(A, B):
    return ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)

def plot(x, y, w, h, b, p, min_dots, max_dots, dwg):

    dots  = []
    verts = []

    # Generate dots
    for i in range(randrange(min_dots, max_dots)):
        dot = (randrange(b, w - b) + x, randrange(b, h - b) + y)
        while dot in dots:
            dot = (randrange(b, w - b), randrange(b, h - b))
        #dwg.add(dwg.circle(dot, 2, fill="white"))
        if len(verts) > 2:
            swing = abs(angle(verts[-2], verts[-1], dot))
            if clear_line((verts[-1], dot), verts) and swing > 120 and swing < 160 and distance(dot, verts[-1]) > 5:
                verts.append(dot)
        else:
            verts.append(dot)
        dots.append(dot)

    # Smooth Cubic bezier path
    c_path = dwg.path(fill_opacity="0", stroke="#3f444a")
    c_path.push('m', verts[0])
    for i in range(2, len(verts), 2):
        c_path.push('S', verts[i-1], verts[i]) 
    dwg.add(c_path)

    # Curve along halves
    c_path = dwg.path(fill_opacity="0", stroke="red")
    c_path.push('M', verts[0])
    c_path.push('L', between(verts[0], verts[1]))
    for i in range(1, len(verts)-1):
        c_path.push('S', verts[i], between(verts[i], verts[i+1]))
    c_path.push('L', verts[-1])
    dwg.add(c_path)

def draw(rows, cols, w, h, b, p, min_dots, max_dots):
    dwg = svgwrite.Drawing('test.svg', profile='tiny')
    for row in range(rows):
        for col in range(cols):
            plot(col * w, row * h, w, h, b, p, min_dots * (row + 1), max_dots * (row + 1), dwg)
    dwg.save()

padding = 0
border  = 25
width   = 500
height  = 2000

min_dots = 25
max_dots = 50

draw(1, 3, width, height, border, padding, min_dots, max_dots)
