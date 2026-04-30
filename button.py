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
        self.text = self.font.render(self.text_input, True, self.text_color)
        filling.draw_filled_polygon(self.surface, self.vertices, self.background_color, self.line_color)
        center_x = sum(v[0] for v in self.vertices) / len(self.vertices)
        center_y = sum(v[1] for v in self.vertices) / len(self.vertices)
        text_rect = self.text.get_rect(center=(center_x, center_y))
        self.surface.blit(self.text, text_rect)

    def checkForInput(self, position):
        """
        Verifica se a posição fornecida (ex: posição do mouse) está dentro
        dos limites do polígono definido pelos vértices.
        Utiliza o algoritmo de Ray Casting.
        """
        x, y = position
        is_inside = False
        n = len(self.vertices)

        # Ponto de partida para o algoritmo
        j = n - 1
        for i in range(n):
            xi, yi = self.vertices[i]
            xj, yj = self.vertices[j]

            # Verifica se o ponto está entre as alturas dos vértices da aresta
            # e se o raio horizontal disparado à direita cruza a aresta
            if ((yi > y) != (yj > y)) and \
                    (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi):
                is_inside = not is_inside
            j = i

        return is_inside

