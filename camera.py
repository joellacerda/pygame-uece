import transformations

class Camera:
    """
    Representa uma câmera no sistema de Computação Gráfica.
    Coordena a transformação entre o Espaço de Mundo (Janela) e o
    Espaço de Dispositivo (Viewport) usando matrizes homogêneas.
    """
    def __init__(self, window, viewport):
        """
        Inicializa a câmera com as coordenadas de Janela e Viewport.

        Parâmetros:
        window: lista ou tupla [xmin, ymin, xmax, ymax] no mundo real.
        viewport: lista ou tupla [xmin, ymin, xmax, ymax] na tela do Pygame.
        """
        self.window = list(window)
        self.viewport = list(viewport)

    def get_matrix(self):
        """
        Retorna a matriz 3x3 de transformação Janela-Viewport.
        Baseada na lógica de inversão de Y e escala ensinada pelo professor.
        """
        return transformations.window_to_viewport(self.window, self.viewport)

    def pan(self, dx, dy):
        """
        Move a lente da câmera pelo mundo (Translação da Janela).
        """
        self.window[0] += dx
        self.window[2] += dx
        self.window[1] += dy
        self.window[3] += dy

    def zoom(self, factor):
        """
        Aplica zoom em relação ao centro da visualização atual.
        factor < 1.0: Aproxima (Zoom In)
        factor > 1.0: Afasta (Zoom Out)
        """
        width = self.window[2] - self.window[0]
        height = self.window[3] - self.window[1]

        # Encontra o ponto central da janela
        cx = self.window[0] + width / 2
        cy = self.window[1] + height / 2

        # Calcula as novas dimensões
        new_w = width * factor
        new_h = height * factor

        # Define as novas bordas mantendo o centro
        self.window[0] = cx - new_w / 2
        self.window[2] = cx + new_w / 2
        self.window[1] = cy - new_h / 2
        self.window[3] = cy + new_h / 2

    def apply(self, points):
        """
        Facilitador para aplicar a visualização da câmera a uma lista de pontos.
        """
        matrix = self.get_matrix()
        return transformations.apply_transformation(matrix, points)
