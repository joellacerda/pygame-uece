import pygame
import primitives
import filling

# pygame setup
pygame.init()
screen = primitives.screen
clock = pygame.time.Clock()
running = True



# 1. CARREGA AS FOTOS
# Entra na pasta 'assets\professores' e pega o arquivo
# matriz_guy, w_guy, h_guy = texture.load_texture("assets/professores/prof_guy_barroso.jpg")


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    #BLUE = (0, 0, 255)
    #RED = (255, 0, 0)
    #primitives.draw_line(20, 20, 200, 400, BLUE)
    #primitives.draw_circle(180, 180, 50, BLUE)
    #square = [(100, 100), (300, 100), (300, 300), (100, 300)]
    #triangle = [(200, 100), (600, 100), (400, 500)]
    #primitives.draw_polygon(square, BLUE)
    #filling.flood_fill(200, 200, RED)
    #filling.draw_filled_polygon(triangle, BLUE, RED)
    #primitives.draw_ellipse(400, 300, 150, 80, (0, 255, 0)) # Desenha uma elipse verde

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()