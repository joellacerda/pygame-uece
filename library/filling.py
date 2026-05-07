from . import primitives

def scanline_fill(surface, vertices, color):
    """"
    Algoritmo de preenchimento Scanline otimizado.

    Parâmetros:
    vertices: Lista de tuplas com os pontos (x, y) do polígono.
    color: Tupla RGB representando a cor de preenchimento.
    """
    # Encontra Y mínimo e máximo
    ys = [v[1] for v in vertices]
    y_min = min(ys)
    y_max = max(ys)

    n = len(vertices)

    for y in range(y_min, y_max):
        intersecoes_x = []

        for i in range(n):
            x0, y0 = vertices[i]
            x1, y1 = vertices[(i + 1) % n]

            # Ignora arestas horizontais
            if y0 == y1:
                continue

            # Garante y0 < y1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0

            # Regra Ymin ≤ y < Ymax
            if y < y0 or y >= y1:
                continue

            # Calcula interseção
            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersecoes_x.append(x)

        # Ordena interseções
        intersecoes_x.sort()

        # Preenche entre pares
        for i in range(0, len(intersecoes_x), 2):
            if i + 1 < len(intersecoes_x):
                x_inicio = int(round(intersecoes_x[i]))
                x_fim = int(round(intersecoes_x[i + 1]))

                for x in range(x_inicio, x_fim + 1):
                    primitives.set_pixel(surface, x, y, color)


def scanline_fill_gradient(surface, vertices, colors):
    """
    Algoritmo de preenchimento Scanline com suporte a gradiente por vértice.
    Interpola as cores ao longo das arestas (Y) e depois ao longo da linha de varredura (X).
    """

    ys = [v[1] for v in vertices]
    y_min = int(min(ys))
    y_max = int(max(ys))
    n = len(vertices)

    for y in range(y_min, y_max):
        intersections = []
        for i in range(n):
            p0, p1 = vertices[i], vertices[(i + 1) % n]
            c0, c1 = colors[i], colors[(i + 1) % n]

            # Ignora arestas horizontais
            if p0[1] == p1[1]: continue

            # Garante que p0 é o ponto superior (menor Y)
            if p0[1] > p1[1]:
                p0, p1, c0, c1 = p1, p0, c1, c0

            # Verifica se a scanline atual cruza a aresta
            if p0[1] <= y < p1[1]:
                t_edge = (y - p0[1]) / (p1[1] - p0[1])
                x_inter = p0[0] + t_edge * (p1[0] - p0[0])
                color_inter = interpolate_color(c0, c1, t_edge)
                intersections.append((x_inter, color_inter))

        # Ordena as interseções pela coordenada X
        intersections.sort(key=lambda item: item[0])

        # Preenche entre os pares de interseções
        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_start, color_start = intersections[i]
                x_end, color_end = intersections[i + 1]

                # Interpola a cor horizontalmente entre as duas arestas
                dist_x = x_end - x_start
                if dist_x > 0:
                    for x in range(int(x_start), int(x_end) + 1):
                        t_scan = (x - x_start) / dist_x
                        pixel_color = interpolate_color(color_start, color_end, t_scan)
                        primitives.set_pixel(surface, x, y, pixel_color)

def draw_filled_polygon(surface, vertices, fill_color, stroke_color):
    """
    Desenha um polígono completamente preenchido e com contorno.
    Combina o algoritmo Scanline para o interior e o algoritmo de Bresenham
    (via primitives.draw_polygon) para as bordas.

    Parâmetros:
    vertices: Lista de tuplas com os pontos (x, y) do polígono.
    fill_color: Tupla RGB da cor interna (preenchimento).
    stroke_color: Tupla RGB da cor da linha de contorno.
    """
    scanline_fill(surface, vertices, fill_color)
    primitives.draw_polygon(surface, vertices, stroke_color)

def flood_fill(surface, x, y, new_color):
    """
    Algoritmo Flood Fill (Preenchimento por Inundação) otimizado por varredura de linha (Span-based).
    Substitui uma área de cor conectada por uma nova cor.
    Esta versão utiliza os métodos da primitives para manter a consistência da biblioteca.
    """
    # 1. Identifica a cor que será substituída
    target_color = primitives.read_pixel(surface, x, y)

    # Se a cor alvo já é a nova cor ou está fora da tela, encerra
    if target_color == new_color or target_color is None:
        return

    stack = [(x, y)]
    width = surface.get_width()
    height = surface.get_height()

    while stack:
        curr_x, curr_y = stack.pop()

        # --- EXPANSÃO HORIZONTAL ---
        # Encontra o limite esquerdo do segmento da mesma cor
        l = curr_x
        while l >= 0 and primitives.read_pixel(surface, l, curr_y) == target_color:
            primitives.set_pixel(surface, l, curr_y, new_color)
            l -= 1

        # Encontra o limite direito do segmento da mesma cor
        r = curr_x + 1
        while r < width and primitives.read_pixel(surface, r, curr_y) == target_color:
            primitives.set_pixel(surface, r, curr_y, new_color)
            r += 1

        # Agora temos o intervalo preenchido: [l + 1, r - 1]

        # --- BUSCA DE NOVAS SEMENTES (SCANLINE OPTIMIZATION) ---
        # Verifica as linhas imediatamente acima e abaixo
        for y_offset in [-1, 1]:
            next_y = curr_y + y_offset

            if 0 <= next_y < height:
                span_added = False

                # Percorre o intervalo horizontal que acabamos de preencher
                for i in range(l + 1, r):
                    if primitives.read_pixel(surface, i, next_y) == target_color:
                        if not span_added:
                            # Adicionamos APENAS a primeira semente de cada segmento
                            stack.append((i, next_y))
                            span_added = True
                    else:
                        span_added = False

def interpolate_color(c1, c2, t):
    """
    Interpola linearmente entre duas cores RGB baseando-se no fator t (0.0 a 1.0).
    """
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)
    return (r, g, b)
