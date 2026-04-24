import primitives

# Constantes de bits para as regiões (TBRL)
INSIDE = 0  # 0000
LEFT   = 1  # 0001
RIGHT  = 2  # 0010
BOTTOM = 4  # 0100
TOP    = 8  # 1000

def region_code(x, y, xmin, ymin, xmax, ymax):
    """
    Calcula o código da região para um ponto (x,y) em relação à janela.
    """
    code = INSIDE
    if x < xmin: code |= LEFT
    elif x > xmax: code |= RIGHT
    if y < ymin: code |= TOP      # y cresce para baixo no Pygame
    elif y > ymax: code |= BOTTOM
    return code

def cohen_sutherland_clip(x0, y0, x1, y1, window):
    """
    Algoritmo de Recorte de Cohen-Sutherland.
    Retorna uma tupla: (visivel, novo_x0, novo_y0, novo_x1, novo_y1)
    """
    xmin, ymin, xmax, ymax = window
    c0 = region_code(x0, y0, xmin, ymin, xmax, ymax)
    c1 = region_code(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        if not (c0 | c1):
            return True, x0, y0, x1, y1  # A linha está totalmente visível

        if c0 & c1:
            return False, None, None, None, None  # A linha está totalmente fora

        # Escolhe um ponto que está fora da janela
        c_out = c0 if c0 else c1

        # Calcula a interseção
        if c_out & TOP:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
            y = ymin
        elif c_out & BOTTOM:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
            y = ymax
        elif c_out & RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            x = xmax
        elif c_out & LEFT:
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            x = xmin

        # Substitui o ponto fora da janela pelo ponto de interseção e recalcula
        if c_out == c0:
            x0, y0 = x, y
            c0 = region_code(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            c1 = region_code(x1, y1, xmin, ymin, xmax, ymax)

def draw_clipped_polygon(vertices, window, color):
    """
    Desenha o contorno de um polígono, garantindo que apenas as partes
    dentro da janela de recorte sejam desenhadas.
    """
    n = len(vertices)

    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]

        # Corta a aresta atual usando a Janela
        visible, rx0, ry0, rx1, ry1 = cohen_sutherland_clip(
            x0, y0, x1, y1, window
        )

        if visible:
            # Se for visível (total ou parcial), manda pro Bresenham
            primitives.draw_line(int(rx0), int(ry0), int(rx1), int(ry1), color)
