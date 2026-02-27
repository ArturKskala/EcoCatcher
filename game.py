import pygame
import sys
import random
import trashclass
import player
import button
import skinmanager
import skrzynki

EXCHANGE_RATE = 0.2
SKIN_CASE_COST = 10*EXCHANGE_RATE 
SPEED_UPGRADE_COST = 50*EXCHANGE_RATE
ADD_LIVE_UPGRADE_COST = 25*EXCHANGE_RATE
AI_RESEARCH_COST = [
        10*EXCHANGE_RATE,
        20*EXCHANGE_RATE,
        30*EXCHANGE_RATE,
        40*EXCHANGE_RATE,
        50*EXCHANGE_RATE
        ]
AI_IMAGES = [
        'images/ai/lvl1.png',
        'images/ai/lvl2.png',
        'images/ai/lvl3.png',
        'images/ai/lvl4.png',
        'images/ai/lvl5.png',
        ]

WIN_MAIN_STR = 'CONGRATULATION'
WIN_STR = 'You\'ve reasearch enough Ai, that now collects bottles on it own!'

class Game():
    def __init__(self):
        self.money = 0.0
        self.MAX_TRASH = 10 
        info = pygame.display.Info()
        self.WIDTH = info.current_w
        self.HEIGHT = info.current_h
        self.TRASH_WIDTH = 120
        self.TRASH_HEIGHT = 120
        self.lives = 5
        self.ai_research = 0

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("EcoCatcher")

        self.load_images()
        self.init_rectangles()
        self.init_buttons()
        self.zegar = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)
        self.font_big = pygame.font.SysFont(None, 90)

        self.player = player.Player(self.window, self.WIDTH, self.HEIGHT)
        self.s = skrzynki.Skrzynki(self.window,self.zegar, self.font, self.font_big)
        self.skinManager = skinmanager.SkinManager(self.s.get_skins_path())

        self.stan = "menu"
        self.butelki = 0

        self.trash_ar = []
        for i in range(self.MAX_TRASH):
           self.trash_ar.append(trashclass.Trash(self.window, self.WIDTH, self.HEIGHT)) 



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
                    if event.key == pygame.K_m:
                        self.money += 100

                    if event.key == pygame.K_u:
                        self.skinManager.unlock_current_skin()
                        self.player.set_skin(self.skinManager.get_current_skin())

                if self.stan == "menu":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.start_button.isClicked():
                            self.reset_lvl()
                            self.butelki = 0
                            self.stan = "workshop"
                
                if self.stan == "workshop":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.skinManager.previuskin()
                            self.player.set_skin(self.skinManager.get_current_skin())

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            self.skinManager.nextskin()
                            self.player.set_skin(self.skinManager.get_current_skin())

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.go_button.isClicked():
                            if self.player.isUnlocked:
                                self.reset_lvl()
                                self.player.set_scale(1)
                                self.stan = "gra"

                        if self.left_button.isClicked():
                            self.skinManager.previuskin()
                            self.player.set_skin(self.skinManager.get_current_skin())

                        if self.right_button.isClicked():
                            self.skinManager.nextskin()
                            self.player.set_skin(self.skinManager.get_current_skin())
                        
                        if self.create_button.isClicked():
                            if self.money >= SKIN_CASE_COST:
                                self.money -= SKIN_CASE_COST
                                self.money = round(self.money, 1)
                                self.stan = 'opening'
                        
                        if self.butelkomat_button.isClicked():
                            self.exchange()

                        if self.speed_button.isClicked():
                            if self.money >= SPEED_UPGRADE_COST:
                                self.money -= SPEED_UPGRADE_COST
                                self.money = round(self.money, 1)
                                self.player.speed += 5
                
                        if self.life_button.isClicked():
                            if self.money >= ADD_LIVE_UPGRADE_COST:
                                self.money -= ADD_LIVE_UPGRADE_COST
                                self.money = round(self.money, 1)
                                self.lives += 1

                        if self.ai_button.isClicked():
                            if self.money >= AI_RESEARCH_COST[self.ai_research]:
                                self.money -= AI_RESEARCH_COST[self.ai_research]
                                self.money = round(self.money, 1)
                                self.ai_research += 1
                                if self.ai_research >= 5:
                                    self.stan = 'win'
                                else:
                                    self.ai_button.set_img(AI_IMAGES[self.ai_research])

                if self.stan == 'gra':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                       if self.workshop_button.isClicked():
                           self.stan = 'workshop' 

                
                if self.stan == 'opening':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.s.start_chest()

                if self.stan == "gameover":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        sys.exit()

                if self.stan == 'win':
                    # if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                    #     sys.exit()

            # ===== MENU =====
            if self.stan == "menu":
                self.show_menu()
            # ===== GRA =====
            if self.stan == "gra":
                self.update_game()
                self.show_game()
            
            if self.stan == 'opening':
                result = self.s.run()
                if result != None:
                    self.skinManager.unlock_skin(result)
                    self.player.set_skin(self.skinManager.get_current_skin())
                    self.stan = 'workshop'
                    self.s = skrzynki.Skrzynki(self.window,self.zegar, self.font, self.font_big)

            if self.stan == "workshop":
                self.show_workshop()

            # ===== GAME OVER =====
            if self.stan == "gameover":
                self.show_gameover()

            if self.stan == 'win':
                self.show_win()

#            self.window.blit(self.font.render(f'FPS: {self.zegar.get_fps()}', 1, (0,255,0)), (self.WIDTH - 200, 0))
            pygame.display.update()


    def update_game(self):
         self.player.move()
         for trash in self.trash_ar:
            trash.update()
            if trash.rect.y > self.HEIGHT+200:
                self.trash_ar.remove(trash)
                self.trash_ar.append(trashclass.Trash(self.window,self.WIDTH, self.HEIGHT))
            if trash.hibox.colliderect(self.player.hitbox):
                self.trash_ar.remove(trash)
                self.trash_ar.append(trashclass.Trash(self.window,self.WIDTH, self.HEIGHT))
                if trash.isBad:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.stan = 'gameover'
                else:
                    self.butelki += 1



    def show_game(self):
        self.window.blit(self.background, (0, 0))
        for trash in self.trash_ar:
            trash.draw()

        wynik = self.font.render("Bottles: " + str(self.butelki), True, (0, 0, 0))
        l = self.font.render('Lives: ' + str(self.lives), True, (0, 0, 0))
        m = self.font.render("Money: " + str(self.money) + "0€", True, (0,0,0))

        self.player.draw_player()
        pygame.draw.rect(self.window, (59,155,63), (0,0,300,150))

        self.workshop_button.draw()
        self.window.blit(wynik, (20, 20))
        self.window.blit(m, (20, 100))
        self.window.blit(l, (20, 60))

    def show_menu(self):
        self.window.blit(self.backgorund_menu, (0, 0))

        # tytul = self.font_big.render("Save our school", True, (255, 255, 255))
        # self.window.blit(tytul, (self.WIDTH / 2 - 250, self.HEIGHT / 3))

        self.start_button.draw()
        self.draw_credits()
    
    def show_workshop(self):
        self.window.blit(self.background_workshop, (0,0))

        self.player.set_scale(2)
        self.player.set_pos(800, 650, 'left')
        self.player.draw_player()

        pygame.draw.rect(self.window, (59,155,63), (self.WIDTH-440, 0, 440, 500)) 

        self.right_button.draw()
        self.left_button.draw()
        self.go_button.draw()
        self.create_button.draw()
        self.butelkomat_button.draw()
        self.speed_button.draw()
        self.life_button.draw()
        self.ai_button.draw()

        pygame.draw.rect(self.window, (59,155,63), (0,0,300,150))
        wynik = self.font.render("Bottles: " + str(self.butelki), True, (0, 0, 0))
        m = self.font.render("Money: " + str(self.money) + "0€", True, (0,0,0))
        l = self.font.render('Lives: ' + str(self.lives), True, (0, 0, 0))
        c = self.font.render(str(SKIN_CASE_COST)+'0€', True, (0,0,0))
        ai_cost = self.font.render(str(AI_RESEARCH_COST[self.ai_research]) + '0€', True, (0,0,0))
        speed_cost = self.font.render(str(SPEED_UPGRADE_COST)+'0€', True, (0,0,0))
        live_cost = self.font.render(str(ADD_LIVE_UPGRADE_COST)+'0€', True, (0,0,0))
        
        
        self.window.blit(speed_cost, (self.WIDTH - 420,100 - speed_cost.get_height()/2))
        self.window.blit(live_cost, (self.WIDTH - 420 ,250 - live_cost.get_height()/2))
        self.window.blit(ai_cost, (self.WIDTH - 420,400 - ai_cost.get_height()/2))

        self.window.blit(c, (1550,620))
        self.window.blit(wynik, (20, 20))
        self.window.blit(l, (20, 60))
        self.window.blit(m, (20, 100))
    
    def reset_lvl(self):
        self.trash_ar = []
        for i in range(self.MAX_TRASH):
           self.trash_ar.append(trashclass.Trash(self.window, self.WIDTH, self.HEIGHT)) 

    def show_win(self):
        self.window.blit(self.backgorund_win, (0,0))

        cień = self.font_big.render(WIN_MAIN_STR, True, (0, 0, 0))
        self.window.blit(cień, (self.WIDTH / 2 - cień.get_width()/2 + 3, self.HEIGHT / 3 + 3))

        napis1 = self.font_big.render(WIN_MAIN_STR, True, (0, 255, 0))
        self.window.blit(napis1, (self.WIDTH / 2 - cień.get_width()/2, self.HEIGHT / 3))

        napis3 = self.font.render(WIN_STR, True, (255, 255, 255))
        self.window.blit(napis3, (self.WIDTH / 2 - napis3.get_width()/2, self.HEIGHT / 2  - napis3.get_height()/2))

    def show_gameover(self):
        self.window.blit(self.background_gameover, (0, 0))

        # GAME OVER z cieniem
        cień = self.font_big.render("GAME OVER", True, (0, 0, 0))
        self.window.blit(cień, (self.WIDTH / 2 - cień.get_width()/2 + 3, self.HEIGHT / 3 + 3))

        napis1 = self.font_big.render("GAME OVER", True, (255, 0, 0))
        self.window.blit(napis1, (self.WIDTH / 2 - napis1.get_width()/2, self.HEIGHT / 3))

        # WRÓCONY NAPIS ZSiPO
        tekst = "Beacause of you the school is covered in trash"
        cień2 = self.font.render(tekst, True, (0, 0, 0))
        self.window.blit(cień2, (self.WIDTH / 2 - cień2.get_width()/2 + 2, self.HEIGHT // 2 + 2))

        napis2 = self.font.render(tekst, True, (255, 255, 255))
        self.window.blit(napis2, (self.WIDTH / 2 - napis2.get_width()/2, self.HEIGHT // 2))

        napis3 = self.font.render("Press ESC to go exit", True, (255, 255, 255))
        self.window.blit(napis3, (self.WIDTH / 2 - napis3.get_width()/2, self.HEIGHT / 2 + 70))

    def init_rectangles(self):
        self.bad_rect = pygame.Rect(random.randint(0, self.WIDTH - 120), random.randint(-self.HEIGHT, 0), self.TRASH_WIDTH, self.TRASH_HEIGHT)

    def load_images(self):
        self.background = pygame.image.load("images/hol.jpg")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.background_gameover = pygame.image.load("images/gameover.png")
        self.background_gameover = pygame.transform.scale(self.background_gameover, (self.WIDTH, self.HEIGHT))
        self.background_workshop = pygame.transform.scale(pygame.image.load("images/workshop.png"), (self.WIDTH, self.HEIGHT))
        self.backgorund_menu = pygame.image.load("images/menu_glowne.png")
        self.backgorund_menu = pygame.transform.scale(self.backgorund_menu, (self.WIDTH, self.HEIGHT))
        self.backgorund_win = pygame.image.load("images/win.png")
        self.backgorund_win = pygame.transform.scale(self.backgorund_win, (self.WIDTH, self.HEIGHT))


    def init_buttons(self):
        self.start_button = button.Button(self.window, pygame.Rect( self.WIDTH / 2 - 200, self.HEIGHT/2 - 200, 400, 400), "images/start.png")
        self.go_button = button.Button(self.window, pygame.Rect(20,self.HEIGHT-170,306,260/2 ), 'images/GO.png')
        self.left_button = button.Button(self.window, pygame.Rect(600,700, 66, 75), 'images/lewo.png')
        self.right_button = button.Button(self.window, pygame.Rect(1200,700, 66, 75), 'images/prawo.png')
        self.create_button = button.Button(self.window, pygame.Rect(self.WIDTH-500,self.HEIGHT-571, 500, 571), 'images/ziutek.png')
        self.workshop_button = button.Button(self.window, pygame.Rect(self.WIDTH-320, self.HEIGHT-100, 300, 85), 'images/workshop_button.png')
        self.butelkomat_button = button.Button(self.window, pygame.Rect(0,self.HEIGHT-732, 408, 612), 'images/Butelkomat.png')
        self.speed_button = button.Button(self.window, pygame.Rect(self.WIDTH - 300, 50, 242, 100), 'images/upgrade.png')
        self.life_button = button.Button(self.window, pygame.Rect(self.WIDTH - 300, 200, 242, 100), 'images/add_life.png')
        self.ai_button = button.Button(self.window, pygame.Rect(self.WIDTH - 300, 350, 242, 100), AI_IMAGES[0])
    
    def exchange(self):
        self.money += self.butelki*EXCHANGE_RATE
        self.money = round(self.money, 1)
        self.butelki = 0

    def draw_credits(self):
        Credits = ['Authors:',
                   'Artur K.', 
                   'Igor C.', 
                   'Janek K.',
                   'Kacper N.', 
                   'Łukasz Z.']
        fonts = []
        w = 0
        h = 0
        for c in Credits:
            f = self.font.render(c, True, (0,0,0))
            fonts.append(f)
            h += f.get_height()
            if w < f.get_width():
                w = f.get_width()

        x = 1700 
        start_y = self.HEIGHT/2 - 160

        rect = pygame.Rect(x-w/2-30,start_y-30,w+60,h+150)
        pygame.draw.rect(self.window, (146,179,34), rect, border_radius=10)


        for f in fonts:
            self.window.blit(f, (x - f.get_width()/2, start_y))
            start_y += 50
