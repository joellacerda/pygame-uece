import pygame
import math
from library import texture
from library import transformations
from library import filling
from library import primitives

class Card:
    def __init__(self, x, y, width, height, id_professor, texture_professor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = id_professor
        self.texture_professor = texture_professor

        self.state = 0
        self.dirty = True
        self.surface_front = None
        self.surface_back = None

        self.scale_x = 1.0
        self.is_animating = False
        self.shrinking = False

        self.is_hovered = False
        self.was_hovered = False


    def get_vertices(self):
        """Retorna os 4 cantos da carta no mundo 2D baseados na posição absoluta"""
        return [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height)
        ]

    def get_uvs(self):
        return [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]

    def _get_card_polygons(self, is_front):
        polys = {}

        # 1. Sombra
        shadow_offset = 6
        polys['shadow'] = [
            (shadow_offset, shadow_offset), (self.width + shadow_offset, shadow_offset),
            (self.width + shadow_offset, self.height + shadow_offset), (shadow_offset, self.height + shadow_offset)
        ]

        # 2. Borda Externa
        polys['base'] = [(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)]

        # 3. Bordas Internas e Fundo
        p1 = 4
        if not is_front:
            polys['inner_black'] = [(p1, p1), (self.width - p1, p1), (self.width - p1, self.height - p1), (p1, self.height - p1)]
            p2 = 8
            polys['bg'] = [(p2, p2), (self.width - p2, p2), (self.width - p2, self.height - p2), (p2, self.height - p2)]
        else:
            p2 = p1
            polys['bg'] = [(p2, p2), (self.width - p2, p2), (self.width - p2, self.height - p2), (p2, self.height - p2)]

            # Tarja do Nome
            tarja_height = 20
            tarja_y = p2 + 2
            polys['tarja'] = [(p2, tarja_y), (self.width - p2, tarja_y), (self.width - p2, tarja_y + tarja_height), (p2, tarja_y + tarja_height)]
            polys['tarja_line'] = [(p2, tarja_y + tarja_height), (self.width - p2, tarja_y + tarja_height)]

        # 4. Textura
        if is_front:
            tex_margin_x = p2
            tex_start_y = p2 + 20 + 4
            tex_end_y = self.height - p2

            polys['tex'] = [
                (tex_margin_x, tex_start_y),
                (self.width - tex_margin_x, tex_start_y),
                (self.width - tex_margin_x, tex_end_y),
                (tex_margin_x, tex_end_y)
            ]
        else:
            logo_w, logo_h = 64, 84
            cx, cy = self.width / 2, self.height / 2
            polys['tex'] = [(cx - logo_w/2, cy - logo_h/2), (cx + logo_w/2, cy - logo_h/2), (cx + logo_w/2, cy + logo_h/2), (cx - logo_w/2, cy + logo_h/2)]

        return polys, p2

    def _render_polygons(self, surface, is_front, texture_mat, m_transform=None):
        """Pinta os polígonos na tela. Aplica a matriz de transformação se ela existir."""
        GRAY_BG = (128, 128, 135)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        YELLOW = (255, 193, 7)

        border_color = YELLOW if is_front else WHITE
        main_bg_color = (15, 15, 20) if is_front else GRAY_BG

        polys, p2 = self._get_card_polygons(is_front)

        if m_transform is not None:
            for k in polys:
                polys[k] = transformations.apply_transformation(m_transform, polys[k])

        filling.draw_filled_polygon(surface, polys['shadow'], BLACK, BLACK)
        filling.draw_filled_polygon(surface, polys['base'], border_color, border_color)

        if not is_front:
            filling.draw_filled_polygon(surface, polys['inner_black'], BLACK, BLACK)

        filling.draw_filled_polygon(surface, polys['bg'], main_bg_color, main_bg_color)

        if is_front:
            filling.draw_filled_polygon(surface, polys['tarja'], BLACK, BLACK)
            p_line = polys['tarja_line']
            primitives.draw_line(surface, int(p_line[0][0]), int(p_line[0][1]), int(p_line[1][0]), int(p_line[1][1]), YELLOW)

            if m_transform is None:
                try:
                    font = pygame.font.SysFont("Courier", 14, bold=True)
                    clean_name = self.id.replace("_", " ").upper()
                    text = font.render(f"PROF. {clean_name}", True, WHITE)
                    text_rect = text.get_rect(center=(self.width/2, p2 + 2 + 10))
                    surface.blit(text, text_rect)
                except Exception:
                    pass

        texture.scanline_texture(surface, polys['tex'], self.get_uvs(), texture_mat, transparent_color=(0,0,0))

    def pre_render(self, texture_verso):
        shadow_padding = 10
        self.surface_front = pygame.Surface((self.width + shadow_padding, self.height + shadow_padding), pygame.SRCALPHA)
        self.surface_back = pygame.Surface((self.width + shadow_padding, self.height + shadow_padding), pygame.SRCALPHA)

        self._render_polygons(self.surface_back, is_front=False, texture_mat=texture_verso)
        self._render_polygons(self.surface_front, is_front=True, texture_mat=self.texture_professor)

    def start_flip(self):
        self.is_animating = True
        self.shrinking = True

    def start_spin(self):
        import random
        self.is_spinning = True
        self.spin_speed = random.uniform(0.05, 0.15) * random.choice([-1, 1])

    def update(self):
        if self.is_hovered != self.was_hovered:
            self.dirty = True
            self.was_hovered = self.is_hovered

        if not self.is_animating:
            return

        self.dirty = True
        speed = 0.12
        if self.shrinking:
            self.scale_x -= speed
            if self.scale_x <= 0.05:
                self.scale_x = 0.05
                self.shrinking = False
                self.state = 1 if self.state == 0 else 0
        else:
            self.scale_x += speed
            if self.scale_x >= 1.0:
                self.scale_x = 1.0
                self.is_animating = False
                self.dirty = True

    def draw(self, surface, texture_verso):
        if not self.is_animating:
            # Se o mouse estiver em cima E a carta estiver virada para baixo
            if getattr(self, 'is_hovered', False) and self.state == 0:
                cx, cy = self.width / 2, self.height / 2

                m_center = transformations.translation(-cx, -cy)
                m_rot = transformations.rotation(math.radians(-5))
                m_rise = transformations.translation(0, -12)
                m_pos = transformations.translation(cx + self.x, cy + self.y)

                m_final = transformations.multiply_matrices(m_rot, m_center)
                m_final = transformations.multiply_matrices(m_rise, m_final)
                m_final = transformations.multiply_matrices(m_pos, m_final)

                self._render_polygons(surface, False, texture_verso, m_transform=m_final)
            else:
                target = self.surface_back if self.state == 0 else self.surface_front
                if target:
                    surface.blit(target, (self.x, self.y))
            return

        cx, cy = self.width / 2, self.height / 2

        m_center = transformations.translation(-cx, -cy)
        m_scale = transformations.scale(self.scale_x, 1.0)
        m_pos = transformations.translation(cx + self.x, cy + self.y)

        m_final = transformations.multiply_matrices(m_scale, m_center)
        m_final = transformations.multiply_matrices(m_pos, m_final)

        is_front = self.state == 1
        tex_actual = self.texture_professor if is_front else texture_verso

        self._render_polygons(surface, is_front, tex_actual, m_transform=m_final)
