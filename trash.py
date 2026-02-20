import pygame
import random
# self.smiec1_img = pygame.transform.scale(self.smiec1_img, (self.TRASH_WIDTH, self.TRASH_HEIGHT))
# self.smiec2_img = pygame.transform.scale(self.smiec2_img, (self.TRASH_WIDTH, self.TRASH_HEIGHT))
# self.smiec3_img = pygame.transform.scale(self.smiec2_img, (self.TRASH_WIDTH, self.TRASH_HEIGHT))
# self.zly_smiec_img = pygame.transform.scale(self.zly_smiec_img, (self.TRASH_WIDTH, self.TRASH_HEIGHT))

good_imges = [
    "images/smiec4.png",
    "images/smiec2.png",
    "images/smiec3.png"
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
        
        if random.randint(0,1) == 1:
            path = random.choice(bad_images)
        else:
            path = random.choice(good_imges)

        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img, (120, 120))

        x = random.randint(0, self.WIDTH - TRASH_WIDTH)
        y = random.randint(-self.HEIGHT, 0)
        self.rect = pygame.Rect(x, y, TRASH_WIDTH, TRASH_HEIGHT)

    def update(self):
        self.rect.y += 6

        if self.rect.y > self.HEIGHT:
            self.rect.x = random.randint(0, self.WIDTH - 120)
            self.rect.y = random.randint(-300, 0)
            smiec[1] = random.choice(self.dobre)

            srodek_x = self.rect.x + self.TRASH_WIDTH / 2
            dol_y = self.rect.y + self.TRASH_HEIGHT

            # TO MODIFY
            if self.rect.colliderect(self.player.rect):
                self.butelki += 1

                self.rect.x = random.randint(0, self.WIDTH - 120)
                self.rect.y = random.randint(-300, 0)
                smiec[1] = random.choice(self.dobre)

            smiec[0] = self.rect
            self.window.blit(smiec[1], smiec[0])

    def draw(self):
        self.window.blit(self.img, self.rect)