from library import texture
class Card:
    def __init__(self, x, y, width, height, id_professor, texture_professor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = id_professor
        self.texture_professor = texture_professor
        self.state = 0  # 0 para verso, 1 para frente

    def get_vertices(self):
        """Retorna os 4 cantos da carta na tela baseados na posição (x, y)"""
        return [
            (self.x, self.y),  # Superior Esquerdo
            (self.x + self.width, self.y),  # Superior Direito
            (self.x + self.width, self.y + self.height),  # Inferior Direito
            (self.x, self.y + self.height)  # Inferior Esquerdo
        ]

    def get_uvs(self):
        """Retorna o mapeamento da textura (0.0 a 1.0) para os 4 cantos"""
        return [
            (0, 0),  # Canto superior esquerdo da imagem
            (1, 0),  # Canto superior direito
            (1, 1),  # Canto inferior direito
            (0, 1)  # Canto inferior esquerdo
        ]

    def draw(self, surface, texture_verso):
        # Define qual textura usar baseado no estado
        tex_actual = texture_verso if self.state == 0 else self.texture_professor

        texture.scanline_texture(
            surface,
            self.get_vertices(),
            self.get_uvs(),
            tex_actual
        )