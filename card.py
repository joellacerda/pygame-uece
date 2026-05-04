import pygame
from library import texture
from library import transformations

class Card:
    def __init__(self, x, y, width, height, id_professor, texture_professor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = id_professor
        self.texture_professor = texture_professor
        
        self.state = 0  # 0 para verso (Logo da UECE), 1 para frente (Professor)
        self.dirty = True  # Marca se a carta precisa ser redesenhada no tabuleiro
        
        # Superfícies para pre-renderização (Cache para otimização de FPS)
        self.surface_front = None
        self.surface_back = None

        # Variáveis de controle da Animação 2D
        self.scale_x = 1.0
        self.is_animating = False
        self.shrinking = False  # True: encolhendo, False: crescendo

    def pre_render(self, texture_verso):
        """
        Executa o algoritmo scanline_texture apenas uma vez no início do jogo.
        Salva o resultado em cache para não destruir a CPU a cada frame.
        """
        self.surface_front = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface_back = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        local_vertices = [
            (0, 0),
            (self.width, 0),
            (self.width, self.height),
            (0, self.height)
        ]
        uvs = self.get_uvs()

        # Renderiza e guarda na memória
        texture.scanline_texture(self.surface_front, local_vertices, uvs, self.texture_professor)
        texture.scanline_texture(self.surface_back, local_vertices, uvs, texture_verso)

    def get_vertices(self):
        """Retorna os 4 cantos da carta no mundo 2D baseados na posição absoluta"""
        return [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height)
        ]

    def get_uvs(self):
        """Retorna o mapeamento da textura (0.0 a 1.0)"""
        return [
            (0.0, 0.0),  # Canto superior esquerdo
            (1.0, 0.0),  # Canto superior direito
            (1.0, 1.0),  # Canto inferior direito
            (0.0, 1.0)   # Canto inferior esquerdo
        ]

    def start_flip(self):
        """Aciona o gatilho para a animação começar no próximo frame"""
        self.is_animating = True
        self.shrinking = True

    def update(self):
        """
        Motor da animação: Chamado a cada frame pelo tabuleiro.
        Altera a escala da carta para simular a rotação em 3D.
        """
        if not self.is_animating:
            return

        self.dirty = True  # Exige que o fundo seja limpo para desenhar a animação
        speed = 0.12       # Velocidade da virada (ajuste se achar rápido/lento)

        if self.shrinking:
            self.scale_x -= speed
            
            # Chegou no "meio" do giro (escala super fina)
            if self.scale_x <= 0.05:
                self.scale_x = 0.05
                self.shrinking = False  # Começa a crescer
                # Inverte a textura revelando o outro lado
                self.state = 1 if self.state == 0 else 0
        else:
            self.scale_x += speed
            
            # Terminou de abrir a carta
            if self.scale_x >= 1.0:
                self.scale_x = 1.0
                self.is_animating = False

    def draw(self, surface, texture_verso):
        """
        Responsável por exibir a carta. Se estiver animando, calcula matrizes em 
        tempo real. Se estiver parada, usa o cache rápido.
        """
        # ==========================================
        # 1. CARTA PARADA (Usa a pre-renderização rápida)
        # ==========================================
        if not self.is_animating:
            # target_surface = self.surface_back if self.state == 0 else self.surface_front
            target_surface = self.surface_back if self.state == 0 else self.surface_front
            
            if target_surface:
                # Otimização suprema: apenas joga a matriz pronta na tela
                surface.blit(target_surface, (self.x, self.y))
            return

        # ==========================================
        # 2. CARTA ANIMANDO (Usa Álgebra Linear exigida no trabalho)
        # ==========================================
        # Vértices locais (centrados na origem local da carta)
        base_vertices = [
            (0, 0),
            (self.width, 0),
            (self.width, self.height),
            (0, self.height)
        ]

        # Calculando o pivô (centro geométrico da carta)
        cx = self.width / 2
        cy = self.height / 2

        # a) T1: Translação para a origem (pivô no 0,0)
        m_center = transformations.translation(-cx, -cy)
        
        # b) S: Escala achatando o eixo X (baseado na animação)
        m_scale = transformations.scale(self.scale_x, 1.0)
        
        # c) T2: Translação de volta, mas agora direto para a posição ABSOLUTA no tabuleiro
        m_pos = transformations.translation(cx + self.x, cy + self.y)

        # Matriz Composta (T2 * S * T1)
        m_temp = transformations.multiply_matrices(m_scale, m_center)
        m_final = transformations.multiply_matrices(m_pos, m_temp)
        
        # Aplica a matriz composta aos vértices base
        anim_vertices = transformations.apply_transformation(m_final, base_vertices)

        # Define qual textura vai mapear no polígono espremido
        tex_actual = texture_verso if self.state == 0 else self.texture_professor
        
        # O poderoso Rasterizador em tempo real entra em ação!
        texture.scanline_texture(surface, anim_vertices, self.get_uvs(), tex_actual)