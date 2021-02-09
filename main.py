import pygame
from sprite import Player, Mob
from os import path

#Definiendo constantes
WIDTH = 480
HEIGHT = 600
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)

#Inicializando directorio de imagenes
img_dir = path.join(path.dirname(__file__),'img')

#Inicializando pygame y creando la ventana
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Mi Juego")
clock = pygame.time.Clock()
font_name =pygame.font.match_font('arial')

#Creando funcion de puntuacion del juego
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def newMob():
    m = Mob(WIDTH,HEIGHT)
    all_sprites.add(m)
    mobs.add(m)

#Funcion que crea la barra de vida del jugador
def draw_shield_bar(surface, x, y, percent):
    if percent < 0:
        percent = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percent/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, WHITE, fill_rect)
    pygame.draw.rect(surface, BLUE, outline_rect, 2)


#Inicializando imagen para el fondo de pantalla
background = pygame.image.load(path.join(img_dir,'background-terror.jpg')).convert()
background_rect = background.get_rect()

all_sprites= pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player(WIDTH,HEIGHT)
all_sprites.add(player)

for i in range(8):
   newMob()
    
score = 0

#Bucle Principal del juego
running = True
while running:
    #Mantener bucle corriendo a una velocidad (FPS)
    clock.tick(FPS)
    
    #Procesos de entrada (Tipos de Eventos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Entradas de Teclado
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               running = False
            if event.key == pygame.K_SPACE:
                player.shoot(all_sprites, bullets)

    #Actualizar
    all_sprites.update()

    #Chequea si el jugador golpea a un mob 
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    #Bucle para crear un mob por cada mob destruido
    for hit in hits:
        score += 2
        newMob()

    #Chequea si un mob golpea al jugador
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= 10
        newMob()
        if player.health <= 0:
            running = False

    #Dibujar / Renderizar
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 16, WIDTH/2, 10)
    draw_shield_bar(screen, 5, 5, player.health)

    #Despues de Dibujar todo
    pygame.display.flip()

#Finalmente cerramos pygame
pygame.quit()