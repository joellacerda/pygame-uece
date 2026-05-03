import pygame
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
        self.dirty = True  # Começa como True para o primeiro desenho
        
        # Superfícies para pre-renderização (Cache)
        self.surface_front = None
        self.surface_back = None

    def pre_render(self, texture_verso):
        """
        Executa os algoritmos de scanline pesados apenas uma vez,
        armazenando o resultado em superfícies do Pygame.
        """
        # Cria superfícies vazias com suporte a transparência (alpha)
        self.surface_front = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface_back = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Como as superfícies são locais (0,0), usamos vértices relativos à superfície
        local_vertices = [
            (0, 0),
            (self.width, 0),
            (self.width, self.height),
            (0, self.height)
        ]
        uvs = self.get_uvs()

        # Renderiza a FRENTE (Foto do Professor) usando o algoritmo manual de scanline
        texture.scanline_texture(self.surface_front, local_vertices, uvs, self.texture_professor)

        # Renderiza o VERSO usando o algoritmo manual de scanline
        texture.scanline_texture(self.surface_back, local_vertices, uvs, texture_verso)

    def get_vertices(self):
        """Retorna os 4 cantos da carta na tela baseados na posição (x, y)"""
        return [
            (self.x, self.y),  # Superior Esquerdo
            (self.x + self.width, self.y),  # Superior Direito
            (self.x + self.width, self.y + self.height),  # Inferior Direito
            (self.x, self.y + self.height)  # Inferior Esquerdo
        ]

    def get_uvs(self):
        """Retorna o mapeamento da textura (0,0 a 1,0) para os 4 cantos"""
        return [
            (0, 0),  # Canto superior esquerdo da imagem
            (1, 0),  # Canto superior direito
            (1, 1),  # Canto inferior direito
            (0, 1)  # Canto inferior esquerdo
        ]

    def draw(self, surface, texture_verso):
        """
        Agora o draw apenas faz o blit da superfície já renderizada.
        Muito mais rápido que rodar o scanline todo frame.
        """
        target_surface = self.surface_back if self.state == 0 else self.surface_front
        
        if target_surface:
            # Se já estiver pre-renderizado, usa a versão rápida
            surface.blit(target_surface, (self.x, self.y))
        else:
            # Fallback caso não tenha sido pre-renderizado (mantém o valor educacional)
            tex_actual = texture_verso if self.state == 0 else self.texture_professor
            texture.scanline_texture(
                surface,
                self.get_vertices(),
                self.get_uvs(),
                tex_actual
            )