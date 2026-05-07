from library import primitives, transformations
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

        # Cores atualizadas para combinar com a Status Bar
        self.COLOR_BG = (0, 0, 0)            # Fundo Preto Puro
        self.COLOR_BORDER = (255, 193, 7)    # Borda Amarela (MUSTARD_YELLOW)

        self.COLOR_HIDDEN = (236, 240, 241)  # Carta para baixo (Branco)
        self.COLOR_FLIPPED = (255, 193, 7)   # Carta virada agora (Amarelo)
        self.COLOR_MATCH = (46, 204, 113)    # Par encontrado (Verde)
        self.COLOR_MISMATCH = (231, 76, 60)  # Par errado (Vermelho)

    def draw(self, screen, board):
        """
        Calcula as matrizes e desenha o minimapa na tela principal.
        """
        # 1. A Janela do Mundo (O que a câmera está capturando)
        # Fixamos a câmera para pegar a mesa inteira (Radar estático)
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

            # Aplica a matriz de Escala/Translação para esmagar para o radar
            vertices_mini = transformations.apply_transformation(matriz_camera, vertices_reais)

            # Lógica BLINDADA de cores do status da carta
            if getattr(card, 'is_matched', False):
                # Se a flag foi ativada (Par Acertado), é VERDE e acabou!
                cor = self.COLOR_MATCH
            elif card in board.flipped_cards:
                if getattr(board, 'is_locked', False):
                    # Acabou de errar (Trava ligada) = Vermelho
                    cor = self.COLOR_MISMATCH
                else:
                    # Sendo analisada = Amarelo
                    cor = self.COLOR_FLIPPED
            else:
                # Escondida (Ou no processo de esconder via animação) = Branco
                cor = self.COLOR_HIDDEN

            # Desenha o polígono em miniatura!
            filling.draw_filled_polygon(screen, vertices_mini, cor, (0, 0, 0))
