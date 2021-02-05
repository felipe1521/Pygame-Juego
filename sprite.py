import pygame
import random
from os import path

class Player(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.BLUE = (0,0,255)
        img_dir = path.join(path.dirname(__file__),'img')
        player_img = pygame.image.load(path.join(img_dir,'pumpkin.png')).convert_alpha()

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(60,80))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.width / 2
        self.rect.bottom = self.height - 20

    def update(self):
        self.x_speed = 0
        #Obteniendo la entrada de teclado para realizar movimientos
        keyState = pygame.key.get_pressed()

        if(keyState[pygame.K_LEFT]):
            self.x_speed = -5   
            #Captando colision con la pared izquierda
            if self.rect.left < 0:
                self.x_speed = 0

        if(keyState[pygame.K_RIGHT]):
            self.x_speed = 5
            #Captando colision con la pared derecha
            if self.rect.left > self.width - 50:
                self.x_speed = 0    
        self.rect.x += self.x_speed

    def shoot(self, all_sprites, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def jumpingAround(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.left > self.width - 50:
            self.x_speed = -5
        elif self.rect.left < 0:
            self.x_speed = 5
        elif self.rect.top > self.height - 50:
            self.y_speed = -5
        elif self.rect.bottom < 50:
            self.y_speed = 5
    

class Mob(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.RED = (255,0,0)
        self.width = WIDTH
        self.height = HEIGHT
        self.image = pygame.Surface((40,40))
        self.image.fill(self.RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.width -self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.y_speed = random.randrange(1, 6)
        self.x_speed = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed

        if self.rect.top > self.height + 10 or self.rect.left < -40 or self.rect.left > self.height + 40:
            self.rect.x = random.randrange(self.width -self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.y_speed = random.randrange(1, 6)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.CYAN = (0,255,247)
        self.image = pygame.Surface((10,10))
        self.image.fill(self.CYAN)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.y_speed = -10
    
    def update(self):
        self.rect.y += self.y_speed
        #Se Destruye si pasa el limite top de la pantalla
        if self.rect.bottom < 0:
            self.kill()
