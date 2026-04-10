# Definindo as regiões usando bits (TBRL - Top, Bottom, Right, Left)
INSIDE = 0  # 0000
LEFT   = 1  # 0001
RIGHT  = 2  # 0010
BOTTOM = 4  # 0100
TOP    = 8  # 1000

def compute_outcode(x, y, x_min, y_min, x_max, y_max):
    """
    Calcula o código de região (Outcode) de 4 bits para um ponto (x,y).
    """
    code = INSIDE

    if x < x_min:      # À esquerda da janela
        code |= LEFT
    elif x > x_max:    # À direita da janela
        code |= RIGHT

    if y < y_min:      # Acima da janela
        code |= TOP
    elif y > y_max:    # Abaixo da janela
        code |= BOTTOM

    return code

def cohen_sutherland_clip(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    """
    Recorta uma linha para caber dentro da janela especificada.
    Retorna (novo_x1, novo_y1, novo_x2, novo_y2) se a linha for visível,
    ou None se a linha estiver completamente fora da tela.
    """
    code1 = compute_outcode(x1, y1, x_min, y_min, x_max, y_max)
    code2 = compute_outcode(x2, y2, x_min, y_min, x_max, y_max)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:
            # Aceitação Trivial: ambos os pontos estão dentro
            accept = True
            break
        elif (code1 & code2) != 0:
            # Rejeição Trivial: ambos estão do mesmo lado de fora (ex: os dois acima do topo)
            break
        else:
            # Pelo menos um ponto está fora. Vamos encontrar a interseção.
            x, y = 0.0, 0.0

            # Escolhe o ponto que está fora da janela
            code_out = code1 if code1 != 0 else code2

            # Fórmulas de interseção de reta:
            # y = y1 + m * (x - x1)  -->  m é a inclinação (y2 - y1) / (x2 - x1)
            # x = x1 + (1 / m) * (y - y1)

            if code_out & TOP:           # Interseção com o topo
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & BOTTOM:      # Interseção com a base
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & RIGHT:       # Interseção com a direita
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & LEFT:        # Interseção com a esquerda
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            # Agora substituímos o ponto que estava fora pelo novo ponto na borda
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_outcode(x1, y1, x_min, y_min, x_max, y_max)
            else:
                x2, y2 = x, y
                code2 = compute_outcode(x2, y2, x_min, y_min, x_max, y_max)

    if accept:
        # Se a linha sobreviveu, retornamos as novas coordenadas arredondadas
        return (int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2)))
    else:
        # A linha inteira estava fora, ignoramos
        return None
