import primitives

def scanline_fill(vertices, color):
    """
    Algoritmo de preenchimento Scanline otimizado.
    Utiliza uma Tabela de Arestas Global (GET - Global Edge Table) para organizar
    todas as arestas do polígono baseadas em sua coordenada Y mínima, e uma Tabela
    de Arestas Ativas (AET - Active Edge Table) para processar as interseções
    linha por linha de varredura (scanlines).

    Parâmetros:
    vertices: Lista de tuplas com os pontos (x, y) do polígono.
    color: Tupla RGB representando a cor de preenchimento.
    """
    if not vertices:
        return

    n = len(vertices)
    y_coords = [v[1] for v in vertices]
    y_min = int(min(y_coords))
    y_max = int(max(y_coords))

    # A GET é um dicionário onde a chave é o y_min da aresta
    get = {}
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]

        # Ignora arestas horizontais (não cruzam scanlines de forma útil)
        if p1[1] == p2[1]:
            continue

        # Garante que p1 é o ponto com menor Y (ponto de origem da aresta de cima para baixo)
        if p1[1] > p2[1]:
            p1, p2 = p2, p1

        y_start, y_end = int(p1[1]), int(p2[1])
        x_at_y_min = float(p1[0])
        # Inclinação inversa (1/m): quanto X muda para cada 1 píxel de avanço em Y
        inv_m = (p2[0] - p1[0]) / (p2[1] - p1[1])

        edge = {
            'y_max': y_end,
            'x_current': x_at_y_min,
            'inv_m': inv_m
        }

        if y_start not in get:
            get[y_start] = []
        get[y_start].append(edge)

    # Processar usando a Active Edge Table (AET)
    aet = []

    for y in range(y_min, y_max + 1):
        # Mover arestas da GET para a AET quando alcançamos seu y_min
        if y in get:
            aet.extend(get[y])

        # Remover arestas da AET quando alcançamos seu y_max
        # Usa-se y_max como limite exclusivo para evitar sobreposição de pixels nos vértices
        aet = [edge for edge in aet if edge['y_max'] > y]

        # Ordenar a AET pelo x_current da esquerda para a direita
        aet.sort(key=lambda edge: edge['x_current'])

        # Preencher os pixels na linha horizontal (scanline) entre pares de arestas
        for i in range(0, len(aet), 2):
            if i + 1 < len(aet):
                x_start = int(round(aet[i]['x_current']))
                x_end = int(round(aet[i+1]['x_current']))
                for x in range(x_start, x_end):
                    primitives.set_pixel(x, y, color)

        # Atualizar o x_current para a próxima scanline (y + 1) incrementando a inclinação inversa
        for edge in aet:
            edge['x_current'] += edge['inv_m']

def draw_filled_polygon(vertices, fill_color, stroke_color):
    """
    Desenha um polígono completamente preenchido e com contorno.
    Combina o algoritmo Scanline para o interior e o algoritmo de Bresenham
    (via primitives.draw_polygon) para as bordas.

    Parâmetros:
    vertices: Lista de tuplas com os pontos (x, y) do polígono.
    fill_color: Tupla RGB da cor interna (preenchimento).
    stroke_color: Tupla RGB da cor da linha de contorno.
    """
    scanline_fill(vertices, fill_color)
    primitives.draw_polygon(vertices, stroke_color)

def flood_fill(x, y, new_color):
    """
    Algoritmo Flood Fill (Preenchimento por Inundação) otimizado por varredura de linha (Span-based).
    Substitui uma área de cor conectada por uma nova cor. Em vez de usar recursão simples
    (que pode causar erro de "Stack Overflow" em áreas grandes), utiliza uma pilha (stack)
    para rastrear segmentos horizontais, expandindo para a esquerda e direita, de forma mais eficiente.

    Parâmetros:
    x, y: Coordenadas do ponto inicial (semente) do preenchimento.
    new_color: Tupla RGB da nova cor a ser aplicada.
    """
    target_color = primitives.read_pixel(x, y)

    # Se a cor alvo já é a nova cor (ou está fora da tela), não faz nada
    if target_color == new_color or target_color is None:
        return

    # Pilha armazena tuplas (x, y) que representam o início de um potencial segmento a verificar
    stack = [(x, y)]
    width = primitives.screen.get_width()

    while stack:
        curr_x, curr_y = stack.pop()

        # Expandir pintando para a esquerda até encontrar uma cor diferente ou a borda
        l = curr_x
        while l >= 0 and primitives.read_pixel(l, curr_y) == target_color:
            primitives.set_pixel(l, curr_y, new_color)
            l -= 1

        # Expandir pintando para a direita até encontrar uma cor diferente ou a borda
        r = curr_x + 1
        while r < width and primitives.read_pixel(r, curr_y) == target_color:
            primitives.set_pixel(r, curr_y, new_color)
            r += 1

        # Neste ponto, existe um intervalo horizontal [l+1, r-1] preenchido nesta linha.

        # Função auxiliar para verificar as linhas imediatamente acima e abaixo em busca de novos segmentos
        def check_neighbors(y_offset):
            span_added = False
            for i in range(l + 1, r):
                if primitives.read_pixel(i, curr_y + y_offset) == target_color:
                    if not span_added:
                        stack.append((i, curr_y + y_offset))
                        span_added = True
                else:
                    span_added = False

        if curr_y > 0:
            check_neighbors(-1)  # Verifica linha Acima
        if curr_y < primitives.screen.get_height() - 1:
            check_neighbors(1)   # Verifica linha Abaixo
