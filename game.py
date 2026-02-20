import pygame
import random
import trash
import player

class Game():
    def __init__(self):
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.MAX_TRASH = 1
        self.TRASH_WIDTH = 120
        self.TRASH_HEIGHT = 120


        self.load_images()
        self.dobre = [self.smiec1_img, self.smiec2_img, self.smiec3_img]
        self.init_rectangles()

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("EcoCatcher")

        self.player = player.Player(self.window, self.WIDTH, self.HEIGHT)

        self.font_big = pygame.font.SysFont(None, 90)
        self.font = pygame.font.SysFont(None, 50)

        self.stan = "menu"

        self.butelki = 0

        self.zegar = pygame.time.Clock()

    def run(self):
        run = True
        while run:
            self.zegar.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

                if self.stan == "menu":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.przycisk.collidepoint(event.pos):
                            self.stan = "gra"

                if self.stan == "gameover":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.stan = "menu"
                        butelki = 0

            # ===== MENU =====
            if self.stan == "menu":
                self.show_menu()
            # ===== GRA =====
            if self.stan == "gra":
                self.show_game()
            # ===== SHOP =====
            if self.stan == "shop":
                pass
            # ===== GAME OVER =====
            if self.stan == "gameover":
                self.show_gameover()

            pygame.display.update()
    def update_game(self):
        pass

    def show_game(self):
        self.player.move()
        self.window.blit(self.background, (0, 0))


        self.bad_rect.y += 6

        if self.bad_rect.y > self.HEIGHT:
            self.bad_rect.y = random.randint(-self.HEIGHT, 0)
            self.bad_rect.x = random.randint(0, self.WIDTH - 120)
        if self.bad_rect.colliderect(self.player):
            self.stan = "gameover"
            self.bad_rect.y = random.randint(-self.HEIGHT, 0)
            self.bad_rect.x = random.randint(0, self.WIDTH - 120)
        self.window.blit(self.zly_smiec_img, self.bad_rect) 

        wynik = self.font.render("Bottles: " + str(self.butelki), True, (0, 0, 0))

        napis = self.font.render("Shop", True, (0,0,0))
        self.player.draw_player()
        pygame.draw.rect(self.window, (0,255,0), self.gobutelkomat_rect)
        self.window.blit(napis, (self.gobutelkomat_rect.x + 20, self.gobutelkomat_rect.y + 20))  
        self.window.blit(wynik, (20, 20))

    def show_menu(self):
        self.window.blit(self.background, (0, 0))

        tytul = self.font_big.render("Save our school", True, (0, 0, 0))
        self.window.blit(tytul, (self.WIDTH / 2 - 250, self.HEIGHT / 3))

        pygame.draw.rect(self.window, (0, 180, 0), self.przycisk)

        napis = self.font.render("START", True, (255, 255, 255))
        self.window.blit(napis, (self.przycisk.x + 70, self.przycisk.y + 25))
    
    def show_end(self):
       pass 

    def show_gameover(self):
        self.window.blit(self.background_gameover, (0, 0))

        # GAME OVER z cieniem
        cień = self.font_big.render("GAME OVER", True, (0, 0, 0))
        self.window.blit(cień, (self.WIDTH / 2 - 250 + 3, self.HEIGHT / 3 + 3))

        napis1 = self.font_big.render("GAME OVER", True, (255, 0, 0))
        self.window.blit(napis1, (self.WIDTH / 2 - 250, self.HEIGHT / 3))

        # WRÓCONY NAPIS ZSiPO
        tekst = "Beacause of you the school is covered in trash"
        cień2 = self.font.render(tekst, True, (0, 0, 0))
        self.window.blit(cień2, (self.WIDTH // 2 - 400 + 2, self.HEIGHT // 2 + 2))

        napis2 = self.font.render(tekst, True, (255, 255, 255))
        self.window.blit(napis2, (self.WIDTH // 2 - 400, self.HEIGHT // 2))

        napis3 = self.font.render("Click to go back to menu", True, (255, 255, 255))
        self.window.blit(napis3, (self.WIDTH // 2 - 250, self.HEIGHT / 2 + 70))

    def init_rectangles(self):
        
        self.gobutelkomat_rect = pygame.Rect(self.WIDTH - 300, self.HEIGHT - 200, 250, 100)
        self.przycisk = pygame.Rect( self.WIDTH / 2 - 120, self.HEIGHT / 2, 240, 90)
        self.bad_rect = pygame.Rect(random.randint(0, self.WIDTH - 120), random.randint(-self.HEIGHT, 0), self.TRASH_WIDTH, self.TRASH_HEIGHT)

    def load_images(self):
        self.background = pygame.image.load("images/hol.jpeg")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.background_gameover = pygame.image.load("images/gameover.png")
        self.background_gameover = pygame.transform.scale(self.background_gameover, (self.WIDTH, self.HEIGHT))

