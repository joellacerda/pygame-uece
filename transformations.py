import math

def identidade():
	"""
    Retorna a matriz identidade 3x3.
    Na multiplicação de matrizes, a identidade funciona como o número 1:
    não altera a matriz original. Serve como base neutra.
    """
	return[
	[1,0,0],
	[0,1,0],
	[0,0,1]
	]

def translacao(tx, ty):
	"""
    Cria uma matriz de translação 2D usando coordenadas homogêneas.

    Parâmetros:
    tx: deslocamento no eixo X (positivo vai para direita, negativo para esquerda).
    ty: deslocamento no eixo Y (positivo vai para baixo/cima dependendo do sistema do Pygame).
    """
	return [
	[1,0,tx],
	[0,1,ty],
	[0,0,1]
	]

def escala(sx, sy):
	"""
    Cria uma matriz de escala 2D usando coordenadas homogêneas.

    Parâmetros:
    sx: multiplicador de tamanho no eixo X (ex: 2.0 dobra a largura, 0.5 divide pela metade).
    sy: multiplicador de tamanho no eixo Y.
    """
	return [
	[sx,0,0],
	[0,sy,0],
	[0,0,1]
	]

def rotacao(theta):
	"""
    Cria uma matriz de rotação 2D usando coordenadas homogêneas.

    Parâmetros:
    theta: ângulo de rotação em radianos.
           (Dica: se tiver o ângulo em graus, use math.radians(graus) antes de passar para cá).
    """
	c = math.cos(theta)
	s = math.sin(theta)

	return [
	[c,-s,0],
	[s,c,0],
	[0,0,1]
	]

def cria_transformacao():
	"""
    Inicializa uma nova matriz de transformação cumulativa.
    Começa como a matriz identidade para que outras transformações (translação,
    rotação, escala) possam ser multiplicadas em sequência formando uma animação.
    """
	return identidade()

def multiplica_matrizes(m1, m2):
    """
    Multiplica duas matrizes 3x3.
    Útil para combinar transformações (ex: transladar e depois rotacionar)
    antes de aplicá-las aos vértices, economizando processamento.
    """
    resultado = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                resultado[i][j] += m1[i][k] * m2[k][j]
    return resultado

def aplica_transformacao(matriz, vertices):
    """
    Aplica uma matriz de transformação 3x3 a uma lista de vértices 2D (x, y).
    Retorna uma nova lista com os vértices transformados (convertidos para int).
    """
    novos_vertices = []

    for x, y in vertices:
        # Multiplicando a matriz de transformação pelo vetor coluna [x, y, 1]
        novo_x = matriz[0][0] * x + matriz[0][1] * y + matriz[0][2] * 1
        novo_y = matriz[1][0] * x + matriz[1][1] * y + matriz[1][2] * 1

        # O cálculo da terceira linha (W) é omitido pois em transformações afins padrão ele continua 1.

        # O Pygame e seu "set_pixel" precisam de coordenadas inteiras, então arredondamos
        novos_vertices.append((int(round(novo_x)), int(round(novo_y))))

    return novos_vertices
