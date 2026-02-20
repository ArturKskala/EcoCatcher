import pygame

class Player():
    def __init__(self, window, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.window = window
        self.rect = pygame.Rect(0, self.HEIGHT - 200, 120, 120)
        self.img = pygame.image.load("images/robot.png")
        self.img = pygame.transform.scale(self.img, (120, 120))

    def draw_player(self):
        print("dziala")
        self.window.blit(self.img, self.rect)

    def update(self):
        pass

    def move(self):
        klawisze = pygame.key.get_pressed()

        if klawisze[pygame.K_LEFT] or klawisze[pygame.K_a]:
            self.rect.x -= 20
        if klawisze[pygame.K_RIGHT] or klawisze[pygame.K_d]:
            self.rect.x += 20
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