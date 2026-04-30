from pathlib import Path
from library import *
from card import Card
from button import Button
import pygame
import sys

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((1280, 720))

# CARREGA AS FOTOS: Entra na pasta 'assets\professors' e pega o arquivo
img_uece = pygame.image.load(Path(__file__).parent /"assets"/"professors"/"uece.png").convert_alpha()
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

WRITE = (255, 255, 255)
SEA_DARK_BLUE = (13, 27, 62)
DARK_BLUE_GRAY = (45, 52, 62)
MUSTARD_YELLOW = (255, 193, 7)
ROYAL_DARK_BLUE = (0, 31, 84)
GRAPHITE = (51, 51, 51)

SCREEN_VERTICES = [(0, 0), (1280, 0), (1280, 720), (0, 720)]

def main_menu():
    pygame.display.set_caption("Menu")

    running_menu = True
    while running_menu:

        screen.fill(SEA_DARK_BLUE)
        CENTRAL_SQUARE = [(240, 57), (1040, 57), (1040, 663), (240, 663)]
        filling.draw_filled_polygon(screen, CENTRAL_SQUARE, DARK_BLUE_GRAY, (255, 255, 255))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # MEMORY LEAK
        font_MENU = pygame.font.SysFont("Arial", 60)
        MENU_TEXT = font_MENU.render("MEMORY", True, MUSTARD_YELLOW)
        MENU_TEXT_2 = font_MENU.render("LEAK", True, MUSTARD_YELLOW)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 200))
        MENU_RECT_2 = MENU_TEXT_2.get_rect(center=(640, 270))
        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(MENU_TEXT_2, MENU_RECT_2)

        # BOTÃO INICIAR JOGO
        font_PLAY = pygame.font.SysFont("Arial", 20)
        PLAY_VERTICES = [(540, 410), (740, 410), (740, 460), (540, 460)]
        PLAY_BUTTON = Button(screen, PLAY_VERTICES, "INICIAR JOGO", font_PLAY, WRITE, SEA_DARK_BLUE, WRITE)

        # BOTÃO SAIR
        font_QUIT = pygame.font.SysFont("Arial", 20)
        QUIT_VERTICES = [(540, 510), (740, 510), (740, 560), (540, 560)]
        QUIT_BUTTON = Button(screen, QUIT_VERTICES, "SAIR", font_QUIT, WRITE, SEA_DARK_BLUE, WRITE)

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

if __name__ == "__main__":
    main_menu()