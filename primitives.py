import pygame

#Define a Resolução
screen = pygame.display.set_mode((1280, 720))

#Imprime um pixel na tela
def set_pixel(x, y, color):
    screen.set_at((x, y), color)

#Ler um pixel na tela
def read_pixel(x, y, color):
    return screen.set_at((x, y), color)

#Algoritmo de Bresenham para desenho de retas
def draw_line(x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        set_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx

        if e2 < dx:
            err += dx
            y0 += sy

#Algoritmo de MidPoint para desenho de círculos
def draw_circle(xc, yc, radius, color):
    x = 0
    y = - radius
    p = -radius

    while x < -y:
        if p > 0:
            y += 1
            p += 2 * (x + y) + 1
        else:
            p += 2 * x + 1

        set_pixel(xc + x, yc + y, color)
        set_pixel(xc - x, yc + y, color)
        set_pixel(xc + x, yc - y, color)
        set_pixel(xc - x, yc - y, color)
        set_pixel(xc + y, yc + x, color)
        set_pixel(xc - y, yc + x, color)
        set_pixel(xc + y, yc - x, color)
        set_pixel(xc - y, yc - x, color)
        x += 1

#Algoritmo de Bresenham para desenho de polígonos
def draw_polygon(vertices, color):
    n = len(vertices)
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]
        draw_line(x0, y0, x1, y1, color)