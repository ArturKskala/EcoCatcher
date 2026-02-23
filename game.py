import pygame
import random
import trashclass
import player
import button
import skinmanager
import skrzynki

class Game():
    def __init__(self):
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.MAX_TRASH = 5
        self.TRASH_WIDTH = 120
        self.TRASH_HEIGHT = 120

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("EcoCatcher")

        self.load_images()
        self.init_rectangles()
        self.init_buttons()


        self.player = player.Player(self.window, self.WIDTH, self.HEIGHT)
        self.skinManager = skinmanager.SkinManager()

        self.font_big = pygame.font.SysFont(None, 90)
        self.font = pygame.font.SysFont(None, 50)

        self.stan = "workshop"
        self.butelki = 0

        self.trash_ar = []
        for i in range(self.MAX_TRASH):
           self.trash_ar.append(trashclass.Trash(self.window, self.WIDTH, self.HEIGHT)) 

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
                        if self.start_button.isClicked():
                            self.reset_lvl()
                            self.stan = "gra"
                
                if self.stan == "workshop":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.go_button.isClicked():
                            if self.player.isUnlocked:
                                self.reset_lvl()
                                self.player.set_scale(1)
                                self.stan = "opening"

                        if self.left_button.isClicked():
                            self.skinManager.previuskin()
                            self.player.set_skin(self.skinManager.get_current_skin())
                        if self.right_button.isClicked():
                            self.skinManager.nextskin()
                            self.player.set_skin(self.skinManager.get_current_skin())

                if self.stan == "gameover":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.stan = "menu"
                        butelki = 0

            # ===== MENU =====
            if self.stan == "menu":
                self.show_menu()
            # ===== GRA =====
            if self.stan == "gra":
                self.update_game()
                self.show_game()
            
            if self.stan == 'opening':
                s = skrzynki.Skrzynki(self.window,self.zegar, self.font, self.font_big)
                s.run()
                # opened skin = Skin Class
                # state == 'workshop' 

            if self.stan == "workshop":
                self.show_workshop()
            # ===== GAME OVER =====
            if self.stan == "gameover":
                self.show_gameover()

            self.window.blit(self.font.render(f'FPS: {self.zegar.get_fps()}', 1, (0,255,0)), (self.WIDTH - 200, 0))
            pygame.display.update()


    def update_game(self):
         self.player.move()
         for trash in self.trash_ar:
            trash.update()
            if trash.rect.y > self.HEIGHT:
                self.trash_ar.remove(trash)
                self.trash_ar.append(trashclass.Trash(self.window,self.WIDTH, self.HEIGHT))
            if trash.hibox.colliderect(self.player.hitbox):
                self.trash_ar.remove(trash)
                self.trash_ar.append(trashclass.Trash(self.window,self.WIDTH, self.HEIGHT))
                if trash.isBad:
                    self.stan = 'gameover'
                else:
                    self.butelki += 1


    def show_game(self):
        self.window.blit(self.background, (0, 0))
        for trash in self.trash_ar:
            trash.draw()

        wynik = self.font.render("Bottles: " + str(self.butelki), True, (0, 0, 0))

        self.player.draw_player()

        self.window.blit(wynik, (20, 20))

    def show_menu(self):
        self.window.blit(self.background, (0, 0))

        tytul = self.font_big.render("Save our school", True, (0, 0, 0))
        self.window.blit(tytul, (self.WIDTH / 2 - 250, self.HEIGHT / 3))

        self.start_button.draw()
    
    def show_workshop(self):
        self.window.blit(self.background_workshop, (0,0))

        self.player.set_scale(2)
        self.player.set_pos(800, 650, 'left')
        self.player.draw_player()

        self.right_button.draw()
        self.left_button.draw()
        self.go_button.draw()

    
    def show_end(self):
       pass 

    def reset_lvl(self):
        self.butelki = 0
        self.trash_ar = []
        for i in range(self.MAX_TRASH):
           self.trash_ar.append(trashclass.Trash(self.window, self.WIDTH, self.HEIGHT)) 


    def show_gameover(self):
        self.butelki = 0
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
        self.bad_rect = pygame.Rect(random.randint(0, self.WIDTH - 120), random.randint(-self.HEIGHT, 0), self.TRASH_WIDTH, self.TRASH_HEIGHT)

    def load_images(self):
        self.background = pygame.image.load("images/hol.jpeg")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.background_gameover = pygame.image.load("images/gameover.png")
        self.background_gameover = pygame.transform.scale(self.background_gameover, (self.WIDTH, self.HEIGHT))
        self.background_workshop = pygame.transform.scale(pygame.image.load("images/workshop.png"), (self.WIDTH, self.HEIGHT))


    def init_buttons(self):
        self.start_button = button.Button(self.window, pygame.Rect( self.WIDTH / 2 - 215, self.HEIGHT/2, 430, 117), "images/start.png")
        self.go_button = button.Button(self.window, pygame.Rect(20,self.HEIGHT-170,306,260/2 ), 'images/GO.png')
        self.left_button = button.Button(self.window, pygame.Rect(600,700, 66, 75), 'images/lewo.png')
        self.right_button = button.Button(self.window, pygame.Rect(1200,700, 66, 75), 'images/prawo.png')

    