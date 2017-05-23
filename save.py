import os.path as fs
import pygame,json,inputbox,colors
class SaveGame:
    def __init__(self,filename="save.txt",screen=pygame.Surface((0,0)),override=False):
        self.filename = filename
        if fs.exists(filename) and not override:
            self.__init_with_file()
        else:
            self.__init_new(screen)

    def __init_with_file(self):
        data = json.load(open(self.filename))
        self.name = data["name"]
        self.lives = data["lives"]
        self.room = data["room"]

    def __init_new(self,surface):
        surface.fill(colors.getColor("black"))
        self.name = inputbox.ask(surface,"Name")
        self.lives = 5
        self.room = 0
        self.save()

    def save(self):
        data = {}
        data["name"] = self.name
        data["lives"] = self.lives
        data["room"] = self.room
        json.dump(data,open(self.filename,"w"))
