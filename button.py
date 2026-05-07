from library import filling
class Button():
    def __init__(self, surface, vertices, text_input, font, text_color, background_color, line_color):
        self.surface = surface
        self.vertices = vertices
        self.text_input = text_input
        self.font = font
        self.text_color = text_color
        self.background_color = background_color
        self.line_color = line_color

        # --- OTIMIZAÇÃO: BOUNDING BOX ---
        # Calcula os limites retangulares (AABB) do polígono uma única vez
        self.min_x = min(v[0] for v in self.vertices)
        self.max_x = max(v[0] for v in self.vertices)
        self.min_y = min(v[1] for v in self.vertices)
        self.max_y = max(v[1] for v in self.vertices)

        self.text = self.font.render(self.text_input, True, self.text_color)
        filling.draw_filled_polygon(self.surface, self.vertices, self.background_color, self.line_color)

        center_x = sum(v[0] for v in self.vertices) / len(self.vertices)
        center_y = sum(v[1] for v in self.vertices) / len(self.vertices)
        text_rect = self.text.get_rect(center=(center_x, center_y))
        self.surface.blit(self.text, text_rect)

    def checkForInput(self, position):
        """
        Verifica se a posição fornecida está dentro do botão.
        Implementa colisão hierárquica: Broad Phase (AABB) → Narrow Phase (Ray Casting).
        """
        x, y = position

        # 1. BROAD PHASE (Fase Larga): Teste de Bounding Box Simples
        # Se o ponto estiver fora do retângulo que envolve o botão,
        # nem perdemos tempo com o Ray Casting complexo.
        if not (self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y):
            return False

        # 2. NARROW PHASE (Fase Estreita): Ray Casting
        # Só chega aqui se o ponto estiver "perto" o suficiente.
        is_inside = False
        n = len(self.vertices)
        j = n - 1
        for i in range(n):
            xi, yi = self.vertices[i]
            xj, yj = self.vertices[j]

            if ((yi > y) != (yj > y)) and \
                    (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi):
                is_inside = not is_inside
            j = i

        return is_inside

