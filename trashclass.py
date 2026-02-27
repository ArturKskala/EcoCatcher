import pygame
import random
# self.smiec1_img = pygame.transform.scale(self.smiec1_img, (self.TRASH_WIDTH, self.TRASH_HEIGHT))
# self.smiec2_img = pygame.transform.scale(self.smiec2_img, (self.TRASH_WIDTH, self.TRASH_HEIGHT))
# self.smiec3_img = pygame.transform.scale(self.smiec2_img, (self.TRASH_WIDTH, self.TRASH_HEIGHT))
# self.zly_smiec_img = pygame.transform.scale(self.zly_smiec_img, (self.TRASH_WIDTH, self.TRASH_HEIGHT))

TRASH_CHANCE = 3 # 1/TRASH_CHANCE
good_imges = [
    "images/smiec4.png",
    "images/smiec2.png",
    "images/butelka.png",
    "images/cisowianka.png"
]

bad_images = [
    "images/zly_smiec.png"
]

class Trash():
    def __init__(self, window, WIDTH, HEIGHT):
        TRASH_WIDTH = 120
        TRASH_HEIGHT = 120
        self.window = window
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.speed = random.randint(5,10) 
        
        if random.randint(0,TRASH_CHANCE) == 0:
            path = random.choice(bad_images)
            self.isBad = True 
        else:
            path = random.choice(good_imges)
            self.isBad = False

        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img, (120, 120))

        x = random.randint(0, self.WIDTH - TRASH_WIDTH)
        y = random.randint(-self.HEIGHT, 0)
        self.rect = pygame.Rect(x, y, TRASH_WIDTH, TRASH_HEIGHT)
        self.hibox = pygame.Rect(x, y, TRASH_WIDTH-30, TRASH_HEIGHT-10)

    def update(self):
        self.rect.y += self.speed
        self.hibox.center = self.rect.center

    def draw(self):
#        pygame.draw.rect(self.window, (255,0,0), self.hibox)
        self.window.blit(self.img, self.rect)