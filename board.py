import random
from card import Card
from library import camera


class Board:
    """
    Gerencia a lógica principal do Jogo da Memória.
    Responsável por instanciar as cartas, organizar o grid 6x4, embaralhar,
    e validar as regras de jogo (combinação de pares e turnos).
    """
    def __init__(self, start_x, start_y, card_width, card_height, spacing_x, spacing_y, professors_data, texture_verso):
        """
        Inicializa o tabuleiro.

        Parâmetros:
        start_x, start_y: Coordenadas (x, y) de onde o grid começa a ser desenhado no Mundo.
        card_width, card_height: Dimensões individuais de cada carta.
        spacing_x, spacing_y: Espaçamento (gap) horizontal e vertical entre as cartas.
        professors_data: Lista de tuplas contendo (id_professor, textura_professor).
        texture_verso: Imagem do verso das cartas.
        """
        self.start_x = start_x
        self.start_y = start_y
        self.card_width = card_width
        self.card_height = card_height
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y

        self.cards = []               # Lista com todos os objetos Card instanciados
        self.flipped_cards = []       # Lista temporária que guarda até 2 cartas viradas no turno atual
        self.matches_found = 0        # Contador de pares encontrados
        self.total_pairs = len(professors_data)
        self.is_locked = False        # Trava o tabuleiro enquanto aguarda a animação/delay de cartas erradas
        self.setup_board(professors_data, texture_verso)

    def setup_board(self, professors_data, texture_verso):
        """
        Duplica a lista de professores para criar os pares, embaralha e
        posiciona cada carta matematicamente no grid 6x4.
        """
        # Duplica os dados para formar os pares
        deck = professors_data * 2

        # Embaralha as cartas aleatoriamente
        random.shuffle(deck)

        # O design pede 24 cartas. Usando 12 pares, faremos 4 linhas e 6 colunas.
        columns = 6

        for index, (prof_id, prof_texture) in enumerate(deck):
            # Calcula a linha e coluna atual com base no índice linear
            row = index // columns
            col = index % columns

            # Calcula as coordenadas X e Y reais no Mundo para esta carta específica
            x_pos = self.start_x + (col * (self.card_width + self.spacing_x))
            y_pos = self.start_y + (row * (self.card_height + self.spacing_y))

            # Instancia a carta e adiciona à lista do tabuleiro
            new_card = Card(x_pos, y_pos, self.card_width, self.card_height, prof_id, prof_texture)

            # Pre-renderiza a carta imediatamente após a criação
            new_card.pre_render(texture_verso)

            self.cards.append(new_card)

    def update(self):
        """
        NOVO MÉTODO:
        Repassa o "sinal de tempo" para todas as cartas do tabuleiro.
        Isso faz o motor de animação 2D de cada carta calcular os quadros da rotação.
        """
        for card in self.cards:
            card.update()

    def handle_click(self, mouse_x, mouse_y):
        """
        Processa o clique do mouse. Verifica se alguma carta foi clicada
        e aplica a lógica de jogo (virar, checar par).

        Retorna:
        String indicando o resultado da ação: "IGNORED", "FLIPPED", "MATCH", "MISMATCH"
        """
        # Se o tabuleiro estiver travado (aguardando as cartas desvirarem), ignora o clique
        if self.is_locked:
            return "IGNORED"

        for card in self.cards:
            # Verifica colisão simples via Bounding Box (AABB)
            if (card.x <= mouse_x <= card.x + card.width and card.y <= mouse_y <= card.y + card.height):

                # Ignora se a carta já estiver virada (state 1), já tiver sido encontrada, ou estiver no meio de uma animação
                if card.state == 1 or card.is_animating:
                    return "IGNORED"

                # Inicia a animação de virar a carta
                card.start_flip()
                self.flipped_cards.append(card)

                # Verifica se duas cartas foram viradas neste turno
                if len(self.flipped_cards) == 2:
                    return self.check_match()

                return "FLIPPED"

        return "IGNORED"

    def handle_mouse_motion(self, mouse_x, mouse_y):
        """
        Verifica continuamente se o mouse está sobre alguma carta
        para aplicar o efeito de Hover.
        """
        # Se o jogo estiver travado (errou o par) não faz hover
        if self.is_locked:
            for card in self.cards:
                card.is_hovered = False
            return

        for card in self.cards:
            # Só faz hover em cartas que estão viradas pra baixo (0) e não estão animando
            if card.state == 0 and not card.is_animating:
                if (card.x <= mouse_x <= card.x + card.width and
                    card.y <= mouse_y <= card.y + card.height):
                    card.is_hovered = True
                else:
                    card.is_hovered = False
            else:
                card.is_hovered = False

    def check_match(self):
        """
        Compara as duas cartas viradas no turno atual.
        """
        card1, card2 = self.flipped_cards

        if card1.id == card2.id:
            # É um par! As cartas permanecem no state 1 para sempre.
            card1.is_matched = True
            card2.is_matched = True
            self.matches_found += 1
            self.flipped_cards.clear()
            return "MATCH"
        else:
            # Não é um par. Trava o tabuleiro para que o main.py possa dar um delay
            self.is_locked = True
            return "MISMATCH"

    def reset_mismatch(self):
        """
        Desvira as cartas que não formaram um par e destrava o tabuleiro.
        Deve ser chamado pelo main.py após um pequeno delay (ex: 1 segundo).
        """
        for card in self.flipped_cards:
            # Aciona a animação 3D para as cartas voltarem a ficar escondidas
            card.start_flip()

        self.flipped_cards.clear()
        self.is_locked = False

    def is_game_over(self):
        """Verifica se todos os pares foram encontrados."""
        return self.matches_found == self.total_pairs

    def draw(self, surface, texture_verso, bg_color, camera):
        # Pega a matriz de transformação Janela -> Viewport da câmera
        m_view = camera.get_matrix()

        # Desenha cartas em ordem (Z-Order)
        for card in self.cards:
            if not getattr(card, 'is_hovered', False) and not card.is_animating:
                card.draw(surface, texture_verso, m_view)

        for card in self.cards:
            if getattr(card, 'is_hovered', False) or card.is_animating:
                card.draw(surface, texture_verso, m_view)
