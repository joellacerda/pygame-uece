from pathlib import Path
from board import Board
from library import primitives
from library import filling
from button import Button
import pygame
import sys

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((1280, 720))

# CARREGA AS FOTOS
img_uece = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"logo_uece.png").convert_alpha()
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
    ("santos", img_santos), ("ph", img_paulo), ("pereira", img_pereira),
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
    start_y=152, # Subiu 5 pixels
    card_width=146,
    card_height=131,
    spacing_x=6,
    spacing_y=7,
    professors_data=professors_data,
    texture_verso=img_uece,
)

# --- SUPERFÍCIES DE CACHE PARA UI ---
logo_surface = None
status_surface = None
menu_bg_cache = None

def render_menu_background():
    """ Gera um fundo procedural usando divisões e Flood Fill """
    surf = pygame.Surface((1280, 720))
    surf.fill(SEA_DARK_BLUE)

    # Criamos áreas fechadas com linhas brancas finas
    # Cruzando a tela em X
    primitives.draw_line(surf, 0, 0, 1280, 720, (30, 45, 90))
    primitives.draw_line(surf, 1280, 0, 0, 720, (30, 45, 90))

    # Preenchemos os triângulos resultantes com tons diferentes de azul
    # Nota: O Flood Fill aqui mostra seu valor ao preencher áreas delimitadas por geometria
    filling.flood_fill(surf, 640, 50, (10, 20, 50))      # Topo
    filling.flood_fill(surf, 640, 670, (15, 30, 70))     # Base
    filling.flood_fill(surf, 50, 360, (20, 35, 80))      # Esquerda
    filling.flood_fill(surf, 1230, 360, (20, 35, 80))    # Direita

    return surf

def main_menu():
    global menu_bg_cache
    pygame.display.set_caption("Menu")

    # Gera o fundo apenas se não estiver em cache (Desempenho)
    if menu_bg_cache is None:
        menu_bg_cache = render_menu_background()

    while True:
        # Usa o fundo procedural cacheado
        screen.blit(menu_bg_cache, (0, 0))

        CENTRAL_SQUARE = [(240, 57), (1040, 57), (1040, 663), (240, 663)]
        filling.draw_filled_polygon(screen, CENTRAL_SQUARE, DARK_BLUE_GRAY, WHITE)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        font_MENU = pygame.font.SysFont("Montserrat", 60)
        MENU_TEXT = font_MENU.render("MEMORY", True, MUSTARD_YELLOW)
        MENU_TEXT_2 = font_MENU.render("LEAK", True, MUSTARD_YELLOW)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 200))
        MENU_RECT_2 = MENU_TEXT_2.get_rect(center=(640, 270))
        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(MENU_TEXT_2, MENU_RECT_2)

        font_PLAY = pygame.font.SysFont("Montserrat", 20)
        PLAY_VERTICES = [(540, 410), (740, 410), (740, 460), (540, 460)]
        PLAY_BUTTON = Button(screen, PLAY_VERTICES, "INICIAR JOGO", font_PLAY, WHITE, SEA_DARK_BLUE, WHITE)

        font_QUIT = pygame.font.SysFont("Montserrat", 20)
        QUIT_VERTICES = [(540, 510), (740, 510), (740, 560), (540, 560)]
        QUIT_BUTTON = Button(screen, QUIT_VERTICES, "SAIR", font_QUIT, WHITE, SEA_DARK_BLUE, WHITE)

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

        pygame.display.update()
        clock.tick(60)

# --- SUPERFÍCIES DE CACHE PARA UI ---
logo_surface = None
status_surface = None

def render_logo_static(font_LOGO):
    surf = pygame.Surface((1280, 44))
    LOGO_VERTICES = [(0, 0), (1280, 0), (1280, 44), (0, 44)]
    filling.draw_filled_polygon(surf, LOGO_VERTICES, WHITE, WHITE)
    LOGO_TEXT = font_LOGO.render("UECE MEMORY", True, SEA_DARK_BLUE)
    LOGO_RECT = LOGO_TEXT.get_rect(midleft=(20, 22))
    surf.blit(LOGO_TEXT, LOGO_RECT)
    return surf

def render_status_bar(font_STATUS, matches, total_pairs, elapsed_time):
    surf = pygame.Surface((896, 83)) # Altura diminuída em 10 pixels
    STATUS_RECT_LOCAL = [(0, 0), (886, 0), (886, 73), (0, 73)]
    filling.draw_filled_polygon(surf, STATUS_RECT_LOCAL, BLACK, MUSTARD_YELLOW)

    total_seconds = elapsed_time // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time_str = f"TIME: {minutes:02d}:{seconds:02d}"

    matches_text = font_STATUS.render(f"MATCHES: {matches}/{total_pairs}", True, WHITE)
    time_text = font_STATUS.render(time_str, True, WHITE)

    surf.blit(matches_text, (12, 16))
    surf.blit(time_text, (730, 16))
    return surf

def victory_screen(elapsed_time):
    """Exibe a tela final de vitória com o tempo total."""
    pygame.display.set_caption("THANKS FOR PLAYING!")

    total_seconds = elapsed_time // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time_str = f"TEMPO TOTAL: {minutes:02d}:{seconds:02d}"

    font_TITLE = pygame.font.SysFont("Montserrat", 60)
    font_TIME = pygame.font.SysFont("Montserrat", 30)

    while True:
        screen.fill(SEA_DARK_BLUE)

        # Retângulo central de vitória com linhas MUSTARD_YELLOW
        VICTORY_RECT = [(340, 240), (940, 240), (940, 480), (340, 480)]
        filling.draw_filled_polygon(screen, VICTORY_RECT, DARK_BLUE_GRAY, MUSTARD_YELLOW)

        # Texto "Você Venceu!" e Tempo na cor MUSTARD_YELLOW
        text_victory = font_TITLE.render("Você Venceu!", True, MUSTARD_YELLOW)
        rect_victory = text_victory.get_rect(center=(640, 330))
        screen.blit(text_victory, rect_victory)

        text_time = font_TIME.render(time_str, True, MUSTARD_YELLOW)
        rect_time = text_time.get_rect(center=(640, 410))
        screen.blit(text_time, rect_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                main_menu()

        pygame.display.update()
        clock.tick(60)

def play():
    global logo_surface, status_surface
    pygame.display.set_caption("MEMORY LEAK")

    font_LOGO = pygame.font.SysFont("Montserrat", 20)
    font_STATUS = pygame.font.SysFont("Courier", 16)

    start_ticks = pygame.time.get_ticks()
    elapsed_time = 0
    last_second = -1
    last_matches_count = -1

    logo_surface = render_logo_static(font_LOGO)
    status_surface = render_status_bar(font_STATUS, game_board.matches_found, game_board.total_pairs, 0)

    screen.fill(SEA_DARK_BLUE)
    game_board.draw(screen, img_uece, SEA_DARK_BLUE, force=True)

    game_board.flipped_cards.clear()
    game_board.is_locked = False
    game_board.matches_found = 0

    delay_start_time = 0
    waiting_for_delay = False

    while True:
        current_time = pygame.time.get_ticks()

        # CHAMA O MOTOR DE ANIMAÇÃO AQUI
        game_board.update()

        if not game_board.is_game_over():
            elapsed_time = current_time - start_ticks

        current_second = elapsed_time // 1000

        if waiting_for_delay:
            if current_time - delay_start_time > 1000:
                game_board.reset_mismatch()
                waiting_for_delay = False

        if current_second != last_second or game_board.matches_found != last_matches_count:
            status_surface = render_status_bar(font_STATUS, game_board.matches_found, game_board.total_pairs, elapsed_time)
            last_second = current_second
            last_matches_count = game_board.matches_found

        screen.blit(logo_surface, (0, 0))
        screen.blit(status_surface, (208, 64))

        game_board.draw(screen, img_uece, SEA_DARK_BLUE)

        if game_board.is_game_over():
            pygame.display.update()
            pygame.time.delay(1000)
            victory_screen(elapsed_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                resultado = game_board.handle_click(mouse_x, mouse_y)

                if resultado == "MISMATCH":
                    waiting_for_delay = True
                    delay_start_time = pygame.time.get_ticks()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
