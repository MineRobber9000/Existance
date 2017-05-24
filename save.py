import os.path as fs
import pygame,json,inputbox,colors
class SaveGame:
    def __init__(self,filename="save.txt",screen=pygame.Surface((0,0)),override=False):
        self.filename = filename
        if fs.exists(filename) and not override:
            self.__init_with_file(screen)
        else:
            self.__init_new(screen)

    def __init_with_file(self,surface):
        data = json.load(open(self.filename))
        for k in ("name","room","exit"):
            if not data.get(k,False):
                print "[DEBUG] [ERROR] Invalid save file, making new"
                self.__init_new(surface)
                return
        self.name = data["name"]
        self.room = data["room"]
        self.exit = data["exit"]
        self.save()

    def __init_new(self,surface):
        surface.fill(colors.getColor("black"))
        self.name = inputbox.ask(surface,"Name")
        self.room = 0
        self.exit = False
        self.save()

    def save(self):
        data = {}
        data["name"] = self.name
        data["room"] = self.room
        data["exit"] = self.exit
        json.dump(data,open(self.filename,"w"))

    def __getitem__(self,k):
        return getattr(self,k)
