import pygame

class SkinManager():
    def __init__(self, paths):
        skinlist_path = paths
        self.skinlist = [] 
        self.skinlist.append({'image': 'images/skins/robot.png', 'unlocked': True})
        i = 1
        for skin_path in skinlist_path:
            # img = pygame.image.load(skin_path)
            self.skinlist.append({'image': skin_path, 'unlocked': False})
            i += 1
        self.skinindex = 0
        self.skincount = len(self.skinlist) - 1
        
    def nextskin(self):
        self.skinindex += 1
        if self.skinindex > self.skincount:
            self.skinindex = self.skincount

    def previuskin(self):
        self.skinindex -= 1
        if self.skinindex < 0:
            self.skinindex = 0

    def get_current_skin(self):
        return self.skinlist[self.skinindex]
    
    def unlock_current_skin(self):
        self.skinlist[self.skinindex]['unlocked'] = True

    def unlock_skin(self, img_path):
        try:
            i = self.skinlist.index({'image': img_path, 'unlocked': False})
            self.skinlist[i]['unlocked'] = True
        except:
            pass