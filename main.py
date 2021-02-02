import pygame
from sprite import Player, Mob

#Definiendo constantes
WIDTH = 480
HEIGHT = 600
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)


#Inicializando pygame y creando la ventana
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Mi Juego")
clock = pygame.time.Clock()

all_sprites= pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player(WIDTH,HEIGHT)
all_sprites.add(player)

for i in range(8):
    m = Mob(WIDTH,HEIGHT)
    all_sprites.add(m)
    mobs.add(m)
    


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

    #Chequea si el jugador hit a un mob 
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    #Bucle para crear un mob por cada mob destruido
    for hit in hits:
        m = Mob(WIDTH,HEIGHT)
        all_sprites.add(m)
        mobs.add(m)
    #Chequea si un mob hit al jugador
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    #Dibujar / Renderizar
    screen.fill(BLACK)
    all_sprites.draw(screen)

    #Despues de Dibujar todo
    pygame.display.flip()

#Finalmente cerramos pygame
pygame.quit()