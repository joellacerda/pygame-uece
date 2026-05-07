from pathlib import Path
from board import Board
from library import primitives
from library import filling
from library import camera
from button import Button
import pygame
import sys
import math
from minimap import Minimap

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((1280, 720))

SOUNDS_DIR = Path(__file__).parent / "assets" / "sounds"
IMGS_DIR = Path(__file__).parent / "assets" / "professors"

# CARREGA OS SONS
pygame.mixer.init()
mismatch_sound = pygame.mixer.Sound(str(SOUNDS_DIR / "mismatch.mp3"))
mismatch_sound.set_volume(0.2)
match_sound = pygame.mixer.Sound(str(SOUNDS_DIR / "match.mp3"))
match_sound.set_volume(0.2)
cardflip_sound = pygame.mixer.Sound(str(SOUNDS_DIR / "cardflip (2).mp3"))
cardflip_sound.set_volume(0.4)
no_interaction_sound = pygame.mixer.Sound(str(SOUNDS_DIR / "already_flipped.mp3"))
no_interaction_sound.set_volume(0.4)
victory_sound = pygame.mixer.Sound(str(SOUNDS_DIR / "victory.mp3"))
victory_sound.set_volume(1.0)
bg_music = pygame.mixer.music.load(str(SOUNDS_DIR / "musica(click - C418).mp3"))
pygame.mixer.music.set_volume(0.4)


# CARREGA AS FOTOS
img_uece = pygame.image.load(IMGS_DIR/"logo_uece.png").convert_alpha()
img_paixao = pygame.image.load(IMGS_DIR/"matheus_paixao.png").convert_alpha()
img_guy = pygame.image.load(IMGS_DIR/"guy_barroso.png").convert_alpha()
img_ana = pygame.image.load(IMGS_DIR/"ana_luiza.png").convert_alpha()
img_henrique = pygame.image.load(IMGS_DIR/"henrique.png").convert_alpha()
img_ismayle = pygame.image.load(IMGS_DIR/"ismayle.png").convert_alpha()
img_negreiros = pygame.image.load(IMGS_DIR/"marcos_negreiros.png").convert_alpha()
img_santos = pygame.image.load(IMGS_DIR/"matheus_santos.png").convert_alpha()
img_paulo = pygame.image.load(IMGS_DIR/"paulo_henrique_maia.png").convert_alpha()
img_pereira = pygame.image.load(IMGS_DIR/"pereira.png").convert_alpha()
img_rafael = pygame.image.load(IMGS_DIR/"rafael.png").convert_alpha()
img_rivas = pygame.image.load(IMGS_DIR/"rivas.png").convert_alpha()
img_thelmo = pygame.image.load(IMGS_DIR/"thelmo.png").convert_alpha()

professors_data = [
    ("paixao", img_paixao), ("guy", img_guy), ("ana", img_ana),
    ("henrique", img_henrique), ("ismayle", img_ismayle), ("negreiros", img_negreiros),
    ("matheus", img_santos), ("ph", img_paulo), ("pereira", img_pereira),
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
    start_y=152,
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
    primitives.draw_line(surf, 0, 0, 1280, 720, (30, 45, 90))
    primitives.draw_line(surf, 1280, 0, 0, 720, (30, 45, 90))

    # Preenchemos os triângulos resultantes com tons diferentes de azul
    filling.flood_fill(surf, 640, 50, (10, 20, 50))      # Topo
    filling.flood_fill(surf, 640, 670, (15, 30, 70))     # Base
    filling.flood_fill(surf, 50, 360, (20, 35, 80))      # Esquerda
    filling.flood_fill(surf, 1230, 360, (20, 35, 80))    # Direita

    return surf

def main_menu():
    global menu_bg_cache
    pygame.display.set_caption("Menu")

    if menu_bg_cache is None:
        menu_bg_cache = render_menu_background()

    while True:
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

def render_logo_static(font_LOGO):
    surf = pygame.Surface((1280, 44))
    LOGO_VERTICES = [(0, 0), (1280, 0), (1280, 44), (0, 44)]
    filling.draw_filled_polygon(surf, LOGO_VERTICES, WHITE, WHITE)
    LOGO_TEXT = font_LOGO.render("UECE MEMORY", True, SEA_DARK_BLUE)
    LOGO_RECT = LOGO_TEXT.get_rect(midleft=(20, 22))
    surf.blit(LOGO_TEXT, LOGO_RECT)
    return surf

def render_status_bar(font_STATUS, matches, total_pairs, elapsed_time):
    surf = pygame.Surface((896, 63))
    STATUS_RECT_LOCAL = [(0, 0), (890, 0), (890, 53), (0, 53)]
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

def draw_brazil_flag(surface, x, y, width):
    height = int(width * 14 / 20)

    GREEN = (0, 156, 59)
    YELLOW = (255, 223, 0)
    BLUE = (0, 39, 118)
    WHITE = (255, 255, 255)

    rect_vertices = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
    rect_colors = [
        (0, 180, 70), GREEN, (0, 100, 30), GREEN
    ]
    filling.scanline_fill_gradient(surface, rect_vertices, rect_colors)

    margin = (width / 20.0) * 1.7
    rhombus_vertices = [
        (x + width / 2, y + margin),
        (x + width - margin, y + height / 2),
        (x + width / 2, y + height - margin),
        (x + margin, y + height / 2)
    ]
    filling.scanline_fill(surface, rhombus_vertices, YELLOW)

    radius = (width / 20.0) * 3.5
    cx, cy = x + width / 2, y + height / 2

    circle_vertices = []
    circle_colors = []
    for i in range(37):
        angle = math.radians(i * 10)
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        circle_vertices.append((px, py))

        t = (py - (cy - radius)) / (2 * radius)
        color = filling.interpolate_color((60, 100, 255), BLUE, t)
        circle_colors.append(color)

    filling.scanline_fill_gradient(surface, circle_vertices, circle_colors)
    primitives.draw_circle(surface, int(cx), int(cy), int(radius), BLUE)

    for offset in range(-1, 2):
        primitives.draw_ellipse(
            surface, int(cx), int(cy + radius * 0.2) + offset,
            int(radius * 1.15), int(radius * 0.45), WHITE
        )

def victory_screen(elapsed_time):
    pygame.display.set_caption("THANKS FOR PLAYING!")
    victory_sound = pygame.mixer.Sound(str(SOUNDS_DIR / "victory.mp3"))
    victory_sound.set_volume(0.4)
    victory_sound.play()

    total_seconds = elapsed_time // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time_str = f"TEMPO TOTAL: {minutes:02d}:{seconds:02d}"

    font_TITLE = pygame.font.SysFont("Montserrat", 60)
    font_TIME = pygame.font.SysFont("Montserrat", 30)

    while True:
        screen.fill(SEA_DARK_BLUE)

        VICTORY_RECT = [(340, 180), (940, 180), (940, 540), (340, 540)]
        filling.draw_filled_polygon(screen, VICTORY_RECT, DARK_BLUE_GRAY, MUSTARD_YELLOW)

        draw_brazil_flag(screen, 540, 200, 200)

        text_victory = font_TITLE.render("Você Venceu!", True, MUSTARD_YELLOW)
        rect_victory = text_victory.get_rect(center=(640, 390))
        screen.blit(text_victory, rect_victory)

        text_time = font_TIME.render(time_str, True, MUSTARD_YELLOW)
        rect_time = text_time.get_rect(center=(640, 480))
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

    # Toca a música em loop infinito
    pygame.mixer.music.play(-1)

    start_ticks = pygame.time.get_ticks()
    elapsed_time = 0
    last_second = -1
    last_matches_count = -1

    logo_surface = render_logo_static(font_LOGO)
    status_surface = render_status_bar(font_STATUS, game_board.matches_found, game_board.total_pairs, 0)

    # Reset do Board
    game_board.flipped_cards.clear()
    game_board.is_locked = False
    game_board.matches_found = 0

    delay_start_time = 0
    waiting_for_delay = False
    celebration_start = 0

    # Instanciando UI e Câmera
    radar = Minimap(20, 64, 150, 100)
    zoom_level = 1.0
    main_camera = camera.Camera(window=[0, 0, 1280, 720], viewport=[0, 0, 1280, 720])

    # Cria os identificadores para os USEREVENTS
    MISMATCH_EVENT = pygame.USEREVENT + 1
    MATCH_EVENT = pygame.USEREVENT + 2

    while True:
        # ==========================================
        # 1. TRATAMENTO DE INPUTS E EVENTOS
        # ==========================================
        keys = pygame.key.get_pressed()
        pan_speed = 15
        if keys[pygame.K_LEFT]: main_camera.pan(-pan_speed, 0)
        if keys[pygame.K_RIGHT]: main_camera.pan(pan_speed, 0)
        if keys[pygame.K_UP]: main_camera.pan(0, -pan_speed)
        if keys[pygame.K_DOWN]: main_camera.pan(0, pan_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- EVENTOS DE ÁUDIO DO COLEGA ---
            if event.type == MISMATCH_EVENT:
                pygame.time.set_timer(MISMATCH_EVENT, 0)   # cancela o timer
                mismatch_sound.play()

            if event.type == MATCH_EVENT:
                pygame.time.set_timer(MATCH_EVENT, 0)      # cancela o timer
                match_sound.play()

            # --- EVENTOS DE RATO COM CÂMERA (SUA ALTERAÇÃO) ---
            if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Desfazemos o Zoom e o Pan para saber onde o mouse está no MUNDO
                m_view = main_camera.get_matrix()
                sx, sy = m_view[0][0], m_view[1][1]
                tx, ty = m_view[0][2], m_view[1][2]
                world_mouse_x = (mouse_x - tx) / sx
                world_mouse_y = (mouse_y - ty) / sy

                if event.type == pygame.MOUSEMOTION:
                    game_board.handle_mouse_motion(world_mouse_x, world_mouse_y)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    resultado = game_board.handle_click(world_mouse_x, world_mouse_y)

                    if resultado == "MISMATCH":
                        cardflip_sound.play()
                        pygame.time.set_timer(MISMATCH_EVENT, 400) # delay som de erro
                        waiting_for_delay = True
                        delay_start_time = pygame.time.get_ticks() + 400

                    elif resultado == "MATCH":
                        cardflip_sound.play()
                        pygame.time.set_timer(MATCH_EVENT, 400) # delay som acerto
                        waiting_for_delay = True
                        delay_start_time = pygame.time.get_ticks() + 400

                    elif resultado == "IGNORED":
                        no_interaction_sound.play()

                    elif resultado == "FLIPPED":
                        cardflip_sound.play()

            # --- EVENTOS DE ZOOM ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    if zoom_level < 2.0:
                        zoom_level += 0.2
                        main_camera.zoom(0.8)
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    if zoom_level > 0.6:
                        zoom_level -= 0.2
                        main_camera.zoom(1.25)

        # ==========================================
        # 2. ATUALIZAÇÃO DA LÓGICA E ESTADOS
        # ==========================================
        current_time = pygame.time.get_ticks()
        game_board.update()

        if not game_board.is_game_over():
            elapsed_time = current_time - start_ticks

        current_second = elapsed_time // 1000

        # Verifica se o delay de cartas erradas acabou
        if waiting_for_delay and (current_time - delay_start_time > 1000):
            game_board.reset_mismatch()
            waiting_for_delay = False

        # Verifica Game Over
        if game_board.is_game_over():
            if celebration_start == 0:
                celebration_start = current_time

            if current_time - celebration_start > 1500:
                    pygame.display.update()
                    victory_screen(elapsed_time)

        # Atualiza o cache da barra de status se necessário
        if current_second != last_second or game_board.matches_found != last_matches_count:
            status_surface = render_status_bar(font_STATUS, game_board.matches_found, game_board.total_pairs, elapsed_time)
            last_second = current_second
            last_matches_count = game_board.matches_found

        # ==========================================
        # 3. RENDERIZAÇÃO
        # ==========================================
        # A) Fundo
        screen.fill(SEA_DARK_BLUE)

        # B) Mundo do Jogo (Aplica Matrizes da Câmera)
        game_board.draw(screen, img_uece, SEA_DARK_BLUE, main_camera)

        # C) Interface do Usuário (Sempre por cima, ignorando a Câmera)
        screen.blit(logo_surface, (0, 0))
        screen.blit(status_surface, (208, 64))
        radar.draw(screen, game_board)

        # 4. EXIBIÇÃO NO MONITOR
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
