import pygame

# Define a Resolução da janela principal
screen = pygame.display.set_mode((1280, 720))

def set_pixel(x, y, color):
    """
    Pinta um único pixel na tela com a cor especificada.
    Esta é a base para todos os algoritmos de rasterização do trabalho.

    Parâmetros:
    x, y: Coordenadas inteiras do pixel.
    color: Tupla RGB representando a cor (ex: (255, 0, 0) para vermelho).
    """
    if (0 <= x < screen.get_width() and 0 <= y < screen.get_height()):
        screen.set_at((x, y), color)

def read_pixel(x, y):
    """
    Lê a cor de um pixel específico na tela.
    Essencial para o algoritmo de preenchimento Flood Fill, que precisa
    saber a cor atual do pixel para decidir se deve pintá-lo ou não.

    Parâmetros:
    x, y: Coordenadas inteiras do pixel a ser lido.

    Retorna:
    A cor (Color object do Pygame) ou None se estiver fora da tela.
    """
    if (0 <= x < screen.get_width() and 0 <= y < screen.get_height()):
        return screen.get_at((x, y))

def draw_line(x0, y0, x1, y1, color):
    """
    Algoritmo de Bresenham para rasterização de retas.
    Usa apenas matemática inteira (adição, subtração e bitshift) para decidir
    qual é o próximo pixel da reta, sendo extremamente rápido.

    Parâmetros:
    x0, y0: Ponto de origem da reta.
    x1, y1: Ponto de destino da reta.
    color: Tupla RGB da cor da linha.
    """
    # Calcula as distâncias absolutas entre os pontos nos eixos X e Y
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    # Determina a direção do passo (1 para avançar, -1 para retroceder)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    # 'err' é o parâmetro de decisão que define se a linha deve "subir/descer"
    err = dx - dy

    while True:
        set_pixel(x0, y0, color)

        # Se chegou no ponto final, encerra o loop
        if x0 == x1 and y0 == y1:
            break

        # Calcula o erro em dobro para tomar as decisões de deslocamento
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx

        if e2 < dx:
            err += dx
            y0 += sy

def draw_circle(xc, yc, radius, color):
    """
    Algoritmo de MidPoint (Ponto Médio) para rasterização de circunferências.
    Explora a simetria de 8 vias do círculo: calcula as coordenadas para um
    único octante (1/8 do círculo) e espelha os pontos para os outros 7 octantes.

    Parâmetros:
    xc, yc: Coordenadas do centro do círculo.
    radius: Raio do círculo.
    color: Tupla RGB da cor do contorno.
    """
    x = 0
    y = - radius

    # 'p' é o parâmetro de decisão (baseado no raio)
    p = -radius

    while x < -y:
        # Se 'p > 0', o pixel ideal está mais longe do centro, então ajustamos o Y
        if p > 0:
            y += 1
            p += 2 * (x + y) + 1
        else: # O pixel ideal está na mesma linha/coluna, só ajustamos o erro
            p += 2 * x + 1

        # Desenha os 8 pontos simétricos usando o centro (xc, yc) como referência
        set_pixel(xc + x, yc + y, color)
        set_pixel(xc - x, yc + y, color)
        set_pixel(xc + x, yc - y, color)
        set_pixel(xc - x, yc - y, color)
        set_pixel(xc + y, yc + x, color)
        set_pixel(xc - y, yc + x, color)
        set_pixel(xc + y, yc - x, color)
        set_pixel(xc - y, yc - x, color)

        # Avança sempre no eixo X (do topo para o lado)
        x += 1

def draw_polygon(vertices, color):
    """
    Desenha o contorno de um polígono conectando seus vértices.

    Parâmetros:
    vertices: Lista de tuplas com os pontos (x, y) (ex: [(10,10), (50,10), (50,50)]).
    color: Tupla RGB da cor das arestas.
    """
    n = len(vertices)
    for i in range(n):
        x0, y0 = vertices[i]
        # O módulo '% n' garante que o último vértice se conecte de volta ao primeiro
        x1, y1 = vertices[(i + 1) % n]
        draw_line(x0, y0, x1, y1, color)

# TODO: Implementar Algoritmo de Anti-aliasing
