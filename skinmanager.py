import pygame

skinlist_path = [
    "images/skins/roboterasmus1.png",
    "images/skins/gold_robot.png",
    "images/skins/gwagon.png",
    "images/skins/red_bull_better1.png",
    "images/skins/chat1.png",
    "images/skins/terminator.png"
]

class SkinManager():
    def __init__(self):
        # "images/skins/robot.png",
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

    def unlock_skin(self, index):
        self.skinlist[index]['unlocked'] = True