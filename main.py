import pygame
import primitives
import filling
import texture

# pygame setup
pygame.init()
screen = primitives.screen
clock = pygame.time.Clock()
running = True



# CARREGA AS FOTOS: Entra na pasta 'assets\professores' e pega o arquivo
matriz_verso, larg_verso, alt_verso = texture.load_texture("assets\professores\logo_uece.png")

matriz_paixao, larg_paixao, alt_paixao = texture.load_texture("assets\professores\prof_matheus_paixao.png")
matriz_guy, larg_guy, alt_guy = texture.load_texture("assets\professores\prof_guy_barroso.png")
matriz_ana, larg_ana, alt_ana = texture.load_texture("assets\professores\prof_ana_luiza.png")
matriz_henrique, larg_henrique, alt_henrique = texture.load_texture("assets\professores\prof_henrique.png")
matriz_ismayle, larg_ismayle, alt_ismayle = texture.load_texture("assets\professores\prof_ismayle.png")
matriz_marcos, larg_marcos, alt_marcos = texture.load_texture("assets\professores\prof_marcos_negreiros.png")
matriz_matheus, larg_matheus, alt_matheus = texture.load_texture("assets\professores\prof_matheus_santos.png")
matriz_paulo, larg_paulo, alt_paulo = texture.load_texture("assets\professores\prof_paulo_henrique_maia.png")
matriz_pereira, larg_pereira, alt_pereira = texture.load_texture("assets\professores\prof_pereira.png")
matriz_rafael, larg_rafael, alt_rafael = texture.load_texture("assets\professores\prof_rafael.png")
matriz_rivas, larg_rivas, alt_rivas = texture.load_texture("assets\professores\prof_rivas.png")
matriz_thelmo, larg_thelmo, alt_thelmo = texture.load_texture("assets\professores\prof_thelmo.png")

# Adicione o parâmetro 'surface' na função
def desenhar_carta_com_foto(surface, x_base, y_base, largura_carta, altura_carta, matriz_foto, larg_foto, alt_foto, cor_fundo=(255, 255, 255), cor_borda=(0, 0, 0)):
    # 1. Desenha o Polígono da Carta (Fundo e Borda)
    vertices_carta = [
        (x_base, y_base),
        (x_base + largura_carta, y_base),
        (x_base + largura_carta, y_base + altura_carta),
        (x_base, y_base + altura_carta)
    ]

    # Passa a surface para o preenchimento
    filling.draw_filled_polygon(surface, vertices_carta, cor_fundo, cor_borda)

    # 2. Mapeamento da foto
    if matriz_foto is not None:
        razao_x = larg_foto / largura_carta
        razao_y = alt_foto / altura_carta
        razao_unica = min(razao_x, razao_y)

        offset_x_foto = int((larg_foto - (largura_carta * razao_unica)) / 2)
        offset_y_foto = int((alt_foto - (altura_carta * razao_unica)) / 2)

        for i in range(largura_carta):
            for j in range(altura_carta):
                margem = 5
                if i > margem and i < largura_carta - margem and j > margem and j < altura_carta - margem:

                    foto_x = int(i * razao_unica) + offset_x_foto
                    foto_y = int(j * razao_unica) + offset_y_foto

                    foto_x = max(0, min(foto_x, larg_foto - 1))
                    foto_y = max(0, min(foto_y, alt_foto - 1))

                    cor_pixel = matriz_foto[foto_x][foto_y]
                    # Passa a surface para o set_pixel
                    primitives.set_pixel(surface, x_base + i, y_base + j, cor_pixel)
# CLASSE CARTA
class Carta:
    def __init__(self, x, y, id_prof, matriz_foto, w_foto, h_foto):
        self.x = x
        self.y = y
        self.largura = 140
        self.altura = 180
        self.id_prof = id_prof
        self.matriz_foto = matriz_foto
        self.w_foto = w_foto
        self.h_foto = h_foto
        self.estado = 0 # 0 = Verso (UECE), 1 = Virada (Prof), 2 = Par Encontrado

    def desenhar(self, surface, matriz_verso, w_verso, h_verso):
        """A carta usa a função molde acima para se desenhar sozinha"""
        if self.estado == 0:
            # Estado 0: Passa a matriz da logo da UECE (e podemos mudar a cor de fundo do verso aqui)
            desenhar_carta_com_foto(surface, self.x, self.y, self.largura, self.altura, matriz_verso, w_verso, h_verso, cor_fundo=(200, 200, 200))
        else:
            # Estados 1 e 2: Passa a matriz da foto do professor
            desenhar_carta_com_foto(surface, self.x, self.y, self.largura, self.altura, self.matriz_foto, self.w_foto, self.h_foto)


# Cria uma instância da carta na posição X=150, Y=100
carta_teste = Carta(50, 20, "prof_guy_barroso", matriz_guy, larg_guy, alt_guy)
carta_teste2 = Carta(50, 220, "prof_guy_barroso", matriz_guy, larg_guy, alt_guy)

cartas_na_mesa = [carta_teste, carta_teste2] # Se tiver 24, basta colocar todas aqui


# 1. DESENHA A MESA INTEIRA UMA ÚNICA VEZ ANTES DO JOGO COMEÇAR!
screen.fill((40, 100, 60))
for carta in cartas_na_mesa:
    carta.desenhar(screen, matriz_verso, larg_verso, alt_verso)
pygame.display.flip() # Joga o desenho pra tela






while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # fill the screen with a color to wipe away anything from last frame
    #screen.fill("black")
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


    # Desenhamos a primeira carta na posição X=50
    #desenhar_carta_com_foto(30, 100, 150, 200, matriz_paixao, larg_paixao, alt_paixao)
    #desenhar_carta_com_foto(200, 100, 150, 200, matriz_guy, larg_guy, alt_guy)
    #desenhar_carta_com_foto(370, 100, 150, 200, matriz_paixao, larg_paixao, alt_paixao)
    #desenhar_carta_com_foto(540, 100, 150, 200, matriz_guy, larg_guy, alt_guy)



        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for carta in cartas_na_mesa:
                atingiu_x = carta.x <= mouse_x <= (carta.x + carta.largura)
                atingiu_y = carta.y <= mouse_y <= (carta.y + carta.altura)

                if atingiu_x and atingiu_y:

                    # 2. INVERTE O ESTADO
                    if carta.estado == 0:
                        carta.estado = 1
                    else:
                        carta.estado = 0

                    # 3. REDESENHA APENAS A CARTA QUE FOI CLICADA!
                    # O resto da mesa continua lá, não precisamos mexer
                    carta.desenhar(screen, matriz_verso, larg_verso, alt_verso)

                    # Atualiza a tela imediatamente após pintar essa única carta
                    pygame.display.flip()

                    break # Para de procurar colisões




    #pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
