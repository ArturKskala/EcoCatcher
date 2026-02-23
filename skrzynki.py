import pygame
import random
import sys
from PIL import Image


class Skrzynki():
    def __init__(self, window, clock, font, big_font):
        self.skins_with_chances = [
            {"file": "images/skins/gwagon.png", "chance": 25, "bg": (196, 174, 214), "name":"Dziełlo"},
            {"file": "images/skins/red_bull_better1.png", "chance": 10, "bg": (255, 179, 186), "name":"Red Bull Better"},
            {"file": "images/skins/terminator.png", "chance": 2, "bg": (255, 255, 204), "name":"Terminator"},
            {"file": "images/skins/gold_robot.png", "chance": 30, "bg": (174, 198, 255), "name":"Złoty Robot"},
            {"file": "images/skins/roboterasmus1.png", "chance": 31, "bg": (186, 255, 201), "name":"Roboterasmus"},
            {"file": "images/skins/chat1.png", "chance": 2, "bg": (255, 240, 200), "name":"Chat"},
        ]

        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        self.window = window

        self.clock = clock
        self.font = font 
        self.big_font = big_font
        self.center_x = WIDTH / 2
        self.center_y = HEIGHT / 2


        # ================== GIF SKRZYNKI =====================
        self.CHEST_SIZE = 400
        gif = Image.open("images/chest.gif")
        self.frames = []
        self.durations = []

        try:
            while True:
                frame = gif.copy().convert("RGBA")
                duration = gif.info.get("duration", 100)
                pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                pygame_frame = pygame.transform.scale(pygame_frame, (self.CHEST_SIZE, self.CHEST_SIZE))
                self.frames.append(pygame_frame)
                self.durations.append(duration / 1000)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        self.current_frame = 0
        self.frame_timer = 0
        self.gif_playing = False
        self.gif_finished = False
        self.gif_elapsed = 0
        self.gif_total_duration = sum(self.durations)
        self.gif_cut_end = 0.8
        self.gif_play_duration = max(0, self.gif_total_duration - self.gif_cut_end)

        # ====================== SKINY ========================
        self.SKIN_SIZE = 140
        self.SPACE = 20

        # ================== STAN GRY =========================
        self.state = "chest"
        self.roll_skins = []
        self.scroll_x = 0
        self.start_scroll = 0
        self.target_scroll = 0
        self.roll_time = 0
        self.roll_duration = 4
        self.selected_skin_info = None
        self.result_anim_time = 0
        self.result_anim_duration = 1.5
        self.result_scale = 0.1
        self.result_target_screen_ratio = 0.6


        for s in self.skins_with_chances:
            s["original_img"] = pygame.image.load(s["file"]).convert_alpha()
            img = pygame.transform.scale(s["original_img"], (self.SKIN_SIZE, self.SKIN_SIZE))
            bg_surface = pygame.Surface((self.SKIN_SIZE, self.SKIN_SIZE))
            bg_surface.fill(s["bg"])
            bg_surface.blit(img, (0,0))
            s["img"] = bg_surface

    def choose_skin(self):
        total = sum(s["chance"] for s in self.skins_with_chances)
        r = random.uniform(0, total)
        upto = 0
        for s in self.skins_with_chances:
            if upto + s["chance"] >= r:
                return s
            upto += s["chance"]
        return self.skins_with_chances[-1]

    def ease_out_cubic(self, t):
        return 1 - (1 - t)**3


    # ================== FUNKCJE ==========================
    def draw_background(self):
        self.window.fill((22,18,40))

    def draw_chest(self, dt):
        if self.gif_playing:
            gif_elapsed += dt
            if gif_elapsed >= self.gif_play_duration:
                self.current_frame = len(self.frames)-1
                self.gif_playing = False
                self.gif_finished = True
                img = self.frames[self.current_frame]
                rect = img.get_rect(center=(self.center_x, self.center_y))
                self.window.blit(img, rect)
                return rect
            frame_timer += dt
            if frame_timer >= self.durations[self.current_frame]:
                frame_timer = 0
                self.current_frame +=1
                if self.current_frame >= len(self.frames):
                    self.current_frame = len(self.frames)-1
                    self.gif_playing = False
                    self.gif_finished = True
        img = self.frames[self.current_frame]
        rect = img.get_rect(center=(self.center_x, self.center_y))
        self.window.blit(img, rect)
        return rect

    def run(self):
        while True:
            dt = self.clock.tick(60)/1000

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state=="chest":
                        chest_rect = pygame.Rect(self.center_x-self.CHEST_SIZE//2, self.center_y-self.CHEST_SIZE//2, self.CHEST_SIZE, self.CHEST_SIZE)
                        if chest_rect.collidepoint(event.pos):
                            self.gif_playing = True
                            self.gif_finished = False
                            self.gif_elapsed = 0
                            self.state = "opening"

            self.draw_background()

            if self.state=="chest":
                self.draw_chest(dt)
                text = self.font.render("Kliknij skrzynkę", True,(255,255,255))
                self.window.blit(text, (self.center_x-text.get_width()//2, self.center_y+220))

            elif self.state=="opening":
                self.draw_chest(dt)
                if self.gif_finished:
                    # losujemy skin, który faktycznie wypadnie
                    selected_skin_info = self.choose_skin()
                    # generujemy rolkę
                    roll_skins = [self.choose_skin()["img"] for _ in range(160)]
                    # zastępujemy środkowy skin tym, który faktycznie wypadł
                    target_index = 120
                    roll_skins[target_index] = selected_skin_info["img"]
                    scroll_x = 0
                    start_scroll = 0
                    roll_time = 0
                    # Ustawiamy przewijanie tak, by wybrany skin zatrzymał się idealnie pod znacznikiem na środku.
                    target_scroll = target_index * (self.SKIN_SIZE + self.SPACE) + self.SKIN_SIZE // 2
                    self.state="roll"

            elif self.state=="roll":
                roll_time += dt
                t = min(roll_time/self.roll_duration,1)
                scroll_x = start_scroll + (target_scroll-start_scroll)*self.ease_out_cubic(t)

                panel_rect = pygame.Rect(0, self.HEIGHT//2 - 120, self.WIDTH, 240)
                pygame.draw.rect(self.window,(40,40,70),panel_rect)
                pygame.draw.rect(self.window,(255,215,0),(self.center_x-3, self.HEIGHT//2-130,6,260))

                start_x = self.center_x - scroll_x
                for i, skin in enumerate(roll_skins):
                    x = start_x + i*(self.SKIN_SIZE+self.SPACE)
                    y = self.HEIGHT//2 - self.SKIN_SIZE//2
                    pygame.draw.rect(self.window,(60,60,95),(x-10,y-10,self.SKIN_SIZE+20,self.SKIN_SIZE+20),border_radius=8)
                    self.window.blit(skin,(x,y))

                if t>=1:
                    self.state="result"
                    result_anim_time=0
                    result_scale=0.1

            elif self.state=="result":
                result_anim_time += dt
                t = min(result_anim_time/self.result_anim_duration,1)
                scale = result_scale + (self.result_target_screen_ratio - result_scale)*self.ease_out_cubic(t)
                img = selected_skin_info["original_img"]
                orig_w, orig_h = img.get_size()
                target_w = self.WIDTH * scale
                target_h = self.HEIGHT * scale
                fit_ratio = min(target_w / orig_w, target_h / orig_h)
                new_width = max(1, int(orig_w * fit_ratio))
                new_height = max(1, int(orig_h * fit_ratio))
                img_scaled = pygame.transform.smoothscale(img,(new_width,new_height))
                rect = img_scaled.get_rect(center=(self.center_x, self.center_y))
                self.window.blit(img_scaled, rect)

