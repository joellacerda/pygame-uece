from pathlib import Path
from board import Board
from library import *
from card import Card
from button import Button
import pygame
import sys

from library.camera import Camera

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((1280, 720))

# CARREGA AS FOTOS: Entra na pasta 'assets\professors' e pega o arquivo
img_uece = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"CardVerso.png").convert_alpha()
img_paixao = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"matheus_paixao.png").convert_alpha()
img_guy = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"guy_barroso.png").convert_alpha()
img_ana = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"ana_luiza.png").convert_alpha()
img_henrique = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"henrique.png").convert_alpha()
img_ismayle = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"ismayle.png").convert_alpha()
img_negreiros = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"marcos_negreiros.png").convert_alpha()
img_santos = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"matheus_santos.png").convert_alpha()
img_paulo = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"paulo_henrique_maia.png").convert_alpha()
img_pereira = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"pereira.png").convert_alpha()
img_rafael = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"rafael.png").convert_alpha()
img_rivas = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"rivas.png").convert_alpha()
img_thelmo = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"thelmo.png").convert_alpha()

professors_data = [
    ("paixao", img_paixao), ("guy", img_guy), ("ana", img_ana),
    ("henrique", img_henrique), ("ismayle", img_ismayle), ("negreiros", img_negreiros),
    ("santos", img_santos), ("paulo", img_paulo), ("pereira", img_pereira),
    ("rafael", img_rafael), ("rivas", img_rivas), ("thelmo", img_thelmo)
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SEA_DARK_BLUE = (13, 27, 62)
DARK_BLUE_GRAY = (45, 52, 62)
MUSTARD_YELLOW = (255, 193, 7)
ROYAL_DARK_BLUE = (0, 31, 84)
GRAPHITE = (51, 51, 51)

SCREEN_VERTICES = [(0, 0), (1280, 0), (1280, 720), (0, 720)]

game_board = Board(
    start_x=201,
    start_y=157,
    card_width=146,
    card_height=131,
    spacing_x=6,
    spacing_y=7,
    professors_data=professors_data
)

MINIMAP_X = 1135
MINIMAP_Y = 90
MINIMAP_W = 121
MINIMAP_H = 142

minimap_viewport = [
    MINIMAP_X,
    MINIMAP_Y,
    MINIMAP_X + MINIMAP_W,
    MINIMAP_Y + MINIMAP_H
]

minimap_window = [201, 157, 201 + 909, 157 + 546]

minimap_camera = Camera(window=minimap_window, viewport=minimap_viewport)

def main_menu():
    pygame.display.set_caption("Menu")

    while True:

        screen.fill(SEA_DARK_BLUE)
        CENTRAL_SQUARE = [(240, 57), (1040, 57), (1040, 663), (240, 663)]
        filling.draw_filled_polygon(screen, CENTRAL_SQUARE, DARK_BLUE_GRAY, WHITE)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # MEMORY LEAK
        font_MENU = pygame.font.SysFont("Montserrat", 60)
        MENU_TEXT = font_MENU.render("MEMORY", True, MUSTARD_YELLOW)
        MENU_TEXT_2 = font_MENU.render("LEAK", True, MUSTARD_YELLOW)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 200))
        MENU_RECT_2 = MENU_TEXT_2.get_rect(center=(640, 270))
        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(MENU_TEXT_2, MENU_RECT_2)

        # BOTÃO INICIAR JOGO
        font_PLAY = pygame.font.SysFont("Montserrat", 20)
        PLAY_VERTICES = [(540, 410), (740, 410), (740, 460), (540, 460)]
        PLAY_BUTTON = Button(screen, PLAY_VERTICES, "INICIAR JOGO", font_PLAY, WHITE, SEA_DARK_BLUE, WHITE)

        # BOTÃO SAIR
        font_QUIT = pygame.font.SysFont("Montserrat", 20)
        QUIT_VERTICES = [(540, 510), (740, 510), (740, 560), (540, 560)]
        QUIT_BUTTON = Button(screen, QUIT_VERTICES, "SAIR", font_QUIT, WHITE, SEA_DARK_BLUE, WHITE)

        # Processamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # 5. Atualiza o frame
        pygame.display.update()
        clock.tick(60)

def play():
    pygame.display.set_caption("MEMORY LEAKS")
    screen.fill(SEA_DARK_BLUE)
    game_board.draw(screen, img_uece, SEA_DARK_BLUE, force=True)

    # Garante que o tabuleiro está limpo e embaralhado ao iniciar uma nova partida
    game_board.flipped_cards.clear()
    game_board.is_locked = False
    game_board.matches_found = 0
    # Opcional: chamar um game_board.setup_board(professors_data) aqui se quiser
    # que o jogo sempre embaralhe ao sair e voltar do menu.

    # Variáveis para o delay de cartas erradas
    delay_start_time = 0
    waiting_for_delay = False

    # Fontes inicializadas fora do loop para desempenho
    font_LOGO = pygame.font.SysFont("Montserrat", 20)
    font_STATUS = pygame.font.SysFont("Courier", 16)

    while True:
        # 1. Atualizações de Lógica e Tempo (Controle de Estado)
        current_time = pygame.time.get_ticks()

        # Se as cartas viradas estiverem erradas, aguarda 1 segundo e depois as desvira
        if waiting_for_delay:
            if current_time - delay_start_time > 1000: # 1000ms = 1 segundo
                game_board.reset_mismatch()
                waiting_for_delay = False

        # 2. Renderização da Tela Base
        # screen.fill(SEA_DARK_BLUE)

        # -- BARRA SUPERIOR (LOGO) --
        LOGO_VERTICES = [(0, 0), (1280, 0), (1280, 44), (0, 44)]
        filling.draw_filled_polygon(screen, LOGO_VERTICES, WHITE, WHITE)
        LOGO_TEXT = font_LOGO.render("UECE MEMORY", True, SEA_DARK_BLUE)
        # O logo fica alinhado à esquerda como no Figma
        LOGO_RECT = LOGO_TEXT.get_rect(midleft=(20, 22))
        screen.blit(LOGO_TEXT, LOGO_RECT)

        # -- STATUS BAR (PLACAR) --
        STATUS_RECT = [(208, 64), (1104, 64), (1104, 157), (208, 157)]
        # No Figma a borda é amarela e o fundo é preto
        filling.draw_filled_polygon(screen, STATUS_RECT, BLACK, MUSTARD_YELLOW)

        # Textos da Status Bar
        matches_text = font_STATUS.render( f"MATCHES: {game_board.matches_found}/{game_board.total_pairs}", True, WHITE)
        screen.blit(matches_text, (220, 80))

        # 3. Renderização do Tabuleiro de Jogo (O Grid Principal)
        # Por enquanto, chamamos o draw diretamente. Futuramente, a Câmera cuidará disso.
        game_board.draw(screen, img_uece, SEA_DARK_BLUE)

        # 4. Renderização do Minimapa (Opcional por agora, entra na parte de Viewport)
        # MINIMAP_BORDER = [(MINIMAP_X, MINIMAP_Y), (MINIMAP_X+MINIMAP_W, MINIMAP_Y),
        #                   (MINIMAP_X+MINIMAP_W, MINIMAP_Y+MINIMAP_H), (MINIMAP_X, MINIMAP_Y+MINIMAP_H)]
        # filling.draw_filled_polygon(screen, MINIMAP_BORDER, GRAPHITE, MUSTARD_YELLOW)

        # 5. Processamento de Eventos (Inputs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Botão esquerdo
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Envia o clique para o tabuleiro processar
                resultado = game_board.handle_click(mouse_x, mouse_y)

                if resultado == "MISMATCH":
                    # Inicia o cronômetro para o delay antes de desvirar
                    waiting_for_delay = True
                    delay_start_time = pygame.time.get_ticks()

        # 6. Atualização de Tela
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
