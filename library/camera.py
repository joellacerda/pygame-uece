from . import transformations

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

        self.world_min_x = -300
        self.world_max_x = 1600
        self.world_min_y = -300
        self.world_max_y = 1000

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
        # Calcula as novas coordenadas potenciais
        new_x0 = self.window[0] + dx
        new_x2 = self.window[2] + dx
        new_y1 = self.window[1] + dy
        new_y3 = self.window[3] + dy

        # Só aplica o movimento em X se a janela continuar dentro do limite do mundo
        if new_x0 > self.world_min_x and new_x2 < self.world_max_x:
            self.window[0] = new_x0
            self.window[2] = new_x2

        # Só aplica o movimento em Y se a janela continuar dentro do limite do mundo
        if new_y1 > self.world_min_y and new_y3 < self.world_max_y:
            self.window[1] = new_y1
            self.window[3] = new_y3

    def zoom(self, factor):
        """
        Aplica zoom em relação ao centro da visualização atual.
        factor < 1.0: Aproxima (Zoom In)
        factor > 1.0: Afasta (Zoom Out)
        """
        width = self.window[2] - self.window[0]
        height = self.window[3] - self.window[1]
        cx, cy = self.window[0] + width / 2, self.window[1] + height / 2

        new_w, new_h = width * factor, height * factor

        # Evita que o zoom out (afastar) fique maior que o próprio mundo
        if new_w > (self.world_max_x - self.world_min_x):
            return

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
