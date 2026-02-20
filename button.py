import pygame

class Button():
    def __init__(self, window, rect: pygame.Rect, img_path = None):
        self.window = window
        self.rect = rect
        if img_path != None:
            self.isImage = True
            self.img = pygame.image.load(img_path)
            self.img = pygame.transform.scale(self.img, (self.rect.width, self.rect.height))
        else:
            self.isImage = False

    def isClicked(self):   
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False 

    def draw(self, color = None):
        if self.isImage:
            self.window.blit(self.img, self.rect)
        else:
            if color != None:
                pygame.draw.rect(self.window, color, self.rect)
            else:
                raise Exception("No Color")