import pygame
import numpy as np

def load_texture(caminho_da_imagem):
    """
    Carrega uma imagem e a transforma em uma matriz numérica 3D (Largura x Altura x RGB).
    """
    try:
        # Carrega a imagem nativa
        img = pygame.image.load(caminho_da_imagem).convert()
        
        # Converte a imagem em uma matriz numérica do Numpy (Array 3D)
        # O formato fica: matriz[x][y] = (R, G, B)
        matriz_pixels = pygame.surfarray.array3d(img)
        
        # Pega as dimensões (largura e altura) da imagem
        largura = matriz_pixels.shape[0]
        altura = matriz_pixels.shape[1]
        
        return matriz_pixels, largura, altura

    except Exception as e:
        print(f"Erro ao carregar a imagem {caminho_da_imagem}: {e}")
        return None, 0, 0