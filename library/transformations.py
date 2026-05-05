import math
import numpy as np

def identity():
    """
    Retorna a matriz identidade 3x3 como um array NumPy.
    """
    return np.identity(3)

def translation(tx, ty):
    """
    Cria uma matriz de translação 2D em coordenadas homogêneas.
    """
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])

def scale(sx, sy):
    """
    Cria uma matriz de escala 2D em coordenadas homogêneas.
    """
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])

def rotation(theta):
    """
    Cria uma matriz de rotação 2D em coordenadas homogêneas.
    """
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])

def create_transformation():
    return identity()

def multiply_matrices(m1, m2):
    """
    Multiplica duas matrizes usando a otimização do NumPy (@).
    """
    return m1 @ m2

def apply_transformation(matrix, vertices):
    """
    Aplica a matriz de transformação a todos os vértices de uma vez (Vetorização).
    """
    if not vertices:
        return []
    
    # 1. Converte lista de (x, y) para matriz NumPy (N, 2)
    v_array = np.array(vertices)
    
    # 2. Adiciona coluna de 1s para coordenadas homogêneas → (N, 3)
    # Ex: [[x1, y1, 1], [x2, y2, 1], ...]
    ones = np.ones((v_array.shape[0], 1))
    v_homogeneous = np.hstack([v_array, ones])
    
    # 3. Multiplica todos os pontos pela matriz de uma vez
    # v_transformed = V * M^T (ou M * V^T)
    # Usamos '.T' na matriz para alinhar as dimensões (N,3) @ (3,3)
    result = v_homogeneous @ matrix.T
    
    # 4. Retorna apenas as colunas X e Y, convertendo para int
    return [(int(round(x)), int(round(y))) for x, y in result[:, :2]]

def window_to_viewport(window, viewport):
    """
    Gera a matriz de transformação de Janela para Viewport usando NumPy.
    """
    Wxmin, Wymin, Wxmax, Wymax = window
    Vxmin, Vymin, Vxmax, Vymax = viewport

    
    # sx = (Vxmax - Vxmin) / (Wxmax - Wxmin)
    # sy = (Vymin - Vymax) / (Wymax - Wymin)  

    # 1. Escala Direta (Sem inverter Vymin e Vymax)
    sx = (Vxmax - Vxmin) / (Wxmax - Wxmin)
    sy = (Vymax - Vymin) / (Wymax - Wymin)

    # Combinando as transformações: Translada -> Escala -> Translada
    # Lembrete: A ordem de aplicação é da direita para a esquerda na multiplicação
    # Passo 1: Translação Negativa (Leva pro centro 0,0)
    m_trans1 = translation(-Wxmin, -Wymin)

    # Passo 2: Escala (Esmaga para caber no minimapa)
    m_scale  = scale(sx, sy)

    # Passo 3: Translação Positiva (Posiciona no canto da tela)
    # ---> O ERRO ESTAVA AQUI! TEM QUE SER Vymin <---
    m_trans2 = translation(Vxmin, Vymin) 

    # Retorna a multiplicação (T2 * S * T1)
    return m_trans2 @ m_scale @ m_trans1
