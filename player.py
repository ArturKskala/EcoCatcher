import pygame
# 549
# 379

class Player():
    def __init__(self, window, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.window = window
        self.player_width = 549/2.5
        self.player_height = 379/2.5

        self.dir = 'left' # 'right'
        self.rect = pygame.Rect(0, self.HEIGHT - 200, self.player_width, self.player_height)
        # self.lock_rect = pygame.Rect()
        self.hitbox = pygame.Rect(0, self.HEIGHT - 200, self.player_width-40, self.player_height-20)

        self.scale = 1
        self.image_path = "images/skins/robot.png"
        self.img = pygame.image.load(self.image_path)
        self.img = pygame.transform.scale(self.img, (self.player_width*self.scale, self.player_height*self.scale))
        self.lock = pygame.image.load("images/klodka.png")
        self.lock = pygame.transform.scale(self.lock, (100, 154))

        self.isUnlocked = True

    def draw_player(self):
#        pygame.draw.rect(self.window, (255,255,0), self.rect)
#        pygame.draw.rect(self.window, (0,255,0), self.hitbox)
#        pygame.draw.circle(self.window, (0,255,255), self.rect.center, 5)

        if self.dir == 'left':
            self.window.blit(self.img, self.rect)
        else:
            self.window.blit(pygame.transform.flip(self.img, 1, 0), self.rect)

        if not self.isUnlocked:
            self.window.blit(self.lock, pygame.Rect(self.rect.centerx + 50, self.rect.centery, self.img.get_width(), self.img.get_height()))

    def set_skin(self, skin):
        self.image_path = skin['image']
        self.isUnlocked = skin['unlocked']
        self.img = pygame.image.load(self.image_path)
        self.img = pygame.transform.scale(self.img, (self.player_width*self.scale, self.player_height*self.scale))

    def set_scale(self, scale):
        self.scale = scale
        self.img = pygame.image.load(self.image_path)
        self.img = pygame.transform.scale(self.img, (self.player_width*self.scale, self.player_height*self.scale))

    def set_pos(self, x, y, dir = 'left'):
        self.rect.centerx = x
        self.rect.centery = y
        self.dir = dir

    def move(self):
        klawisze = pygame.key.get_pressed()

        if klawisze[pygame.K_LEFT] or klawisze[pygame.K_a]:
            self.rect.x -= 20
            self.dir = 'left'
        if klawisze[pygame.K_RIGHT] or klawisze[pygame.K_d]:
            self.rect.x += 20
            self.dir = 'right'
        if klawisze[pygame.K_UP] or klawisze[pygame.K_w]:
            self.rect.y -= 20
        if klawisze[pygame.K_DOWN] or klawisze[pygame.K_s]:
            self.rect.y += 20


        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > self.WIDTH - 120:
            self.rect.x = self.WIDTH - 120
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > self.HEIGHT - 120:
            self.rect.y = self.HEIGHT - 120
        
        self.hitbox.center = self.rect.center