import pygame
from library import transformations
from library import filling 

class Minimap:
    def __init__(self, view_x, view_y, view_width, view_height):
        """
        Inicializa o Minimapa (O Viewport de destino)
        """
        self.Vxmin = view_x
        self.Vymin = view_y
        self.Vxmax = view_x + view_width
        self.Vymax = view_y + view_height
        self.viewport = (self.Vxmin, self.Vymin, self.Vxmax, self.Vymax)
        
        # Cores padrão do Minimapa
        self.COLOR_BG = (30, 40, 50)         # Fundo escuro do radar
        self.COLOR_BORDER = (241, 196, 15)   # Borda Amarela
        self.COLOR_HIDDEN = (236, 240, 241)  # Carta pra baixo (Branco)
        self.COLOR_FLIPPED = (241, 196, 15)  # Carta virada agora (Amarelo)
        self.COLOR_MATCH = (46, 204, 113)    # Par encontrado (Verde)

    def draw(self, screen, board):
        """
        Calcula as matrizes e desenha o minimapa na tela principal.
        """
        # 1. A Janela do Mundo (O que a câmera está capturando)
        # Fixamos a câmera para pegar a mesa inteira
        Wxmin, Wymin = 180, 130
        Wxmax, Wymax = 1120, 720
        janela_mundo = (Wxmin, Wymin, Wxmax, Wymax)

        # 2. Gera a Matriz de Transformação (Mundo -> Tela)
        matriz_camera = transformations.window_to_viewport(janela_mundo, self.viewport)

        # 3. Desenha o fundo e a borda do Minimapa
        fundo_vertices = [
            (self.Vxmin, self.Vymin), (self.Vxmax, self.Vymin), 
            (self.Vxmax, self.Vymax), (self.Vxmin, self.Vymax)
        ]
        filling.draw_filled_polygon(screen, fundo_vertices, self.COLOR_BG, self.COLOR_BORDER)

        # 4. Desenha as cartas convertidas para o minimapa
        for card in board.cards:
            # Pega as coordenadas gigantes da mesa
            vertices_reais = card.get_vertices()
            
            # Aplica a matriz de Escala/Translação para esmagar pro radar
            vertices_mini = transformations.apply_transformation(matriz_camera, vertices_reais)

            # Lógica de cores do status da carta
            if card.state == 1 and card not in board.flipped_cards:
                cor = self.COLOR_MATCH
            elif card in board.flipped_cards:
                cor = self.COLOR_FLIPPED
            else:
                cor = self.COLOR_HIDDEN

            # Desenha o polígono em miniatura!
            filling.draw_filled_polygon(screen, vertices_mini, cor, (0, 0, 0))