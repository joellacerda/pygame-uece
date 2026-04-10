class Camera:
    def __init__(self, w_min_x, w_min_y, w_max_x, w_max_y, v_min_x, v_min_y, v_max_x, v_max_y):
        # Janela (Coordenadas de Mundo) - A área do tabuleiro que estamos "filmando"
        self.w_min_x = w_min_x
        self.w_min_y = w_min_y
        self.w_max_x = w_max_x
        self.w_max_y = w_max_y

        # Viewport (Coordenadas de Dispositivo) - A área da tela onde o desenho vai aparecer
        self.v_min_x = v_min_x
        self.v_min_y = v_min_y
        self.v_max_x = v_max_x
        self.v_max_y = v_max_y

    def world_to_viewport(self, x_world, y_world):
        """
        Converte um ponto do Mundo Real (tabuleiro) para o Dispositivo (tela do Pygame).
        """
        # Calcula as proporções (escala) entre a Tela e a Janela
        sx = (self.v_max_x - self.v_min_x) / (self.w_max_x - self.w_min_x)
        sy = (self.v_max_y - self.v_min_y) / (self.w_max_y - self.w_min_y)

        # Aplica a fórmula de mapeamento linear
        x_viewport = self.v_min_x + (x_world - self.w_min_x) * sx
        y_viewport = self.v_min_y + (y_world - self.w_min_y) * sy

        return int(round(x_viewport)), int(round(y_viewport))

    def pan(self, dx, dy):
        """
        Move a câmera pelo mundo (Translação da Janela).
        Isso atende ao requisito de interatividade de navegação.
        """
        self.w_min_x += dx
        self.w_max_x += dx
        self.w_min_y += dy
        self.w_max_y += dy

    def zoom(self, factor):
        """
        Aplica zoom na câmera (Escala da Janela).
        Fator < 1: Zoom In (vê menos do mundo, as cartas ficam maiores)
        Fator > 1: Zoom Out (vê mais do mundo, as cartas ficam menores)
        """
        width = self.w_max_x - self.w_min_x
        height = self.w_max_y - self.w_min_y

        # Descobre o centro atual da câmera para dar zoom em direção ao centro
        cx = self.w_min_x + width / 2
        cy = self.w_min_y + height / 2

        nova_largura = width * factor
        nova_altura = height * factor

        # Atualiza as bordas da janela com o novo tamanho
        self.w_min_x = cx - nova_largura / 2
        self.w_max_x = cx + nova_largura / 2
        self.w_min_y = cy - nova_altura / 2
        self.w_max_y = cy + nova_altura / 2
