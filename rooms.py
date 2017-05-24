import pygame,colors
from pygame.locals import *
pygame.font.init()
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

main_font = pygame.font.SysFont("Arial",18)

def prnt(text,surface,x=0,y=0,c=colors.getColor("black")):
    drawText(surface,text,c,main_font.render(text,True,c).get_rect().move(x,y),main_font,True)

class Room(object):
    def __init__(self,name,content):
        self.name = name
        self.content = content

    def drawTo(self,screen=pygame.Surface((0,0)),playername="Existance Player"):
        text = self.name+"\n\n"+self.content
        text = text.format(playername=playername)
        y = 2
        for line in text.split("\n"):
            if line.rstrip():
                prnt(line.rstrip(),screen,2,y)
            y += 20

    def keyDownHandler(self,savegame,key):
        pass

class BasicRoom(Room):
    def __init__(self,name,content):
        super(BasicRoom,self).__init__(name,content)

    def keyDownHandler(self,savegame,key):
        if key == K_RETURN:
            savegame.room += 1
        return savegame

class EndRoom(Room):
    def __init__(self,name,content):
        super(EndRoom,self).__init__(name,content)

    def keyDownHandler(self,savegame,key):
        if key == K_RETURN:
            savegame.exit = True
        return savegame

class Act1Room(Room):
    def __init__(self,name,content,actions={}):
        super(Act1Room,self).__init__(name,content)
        if actions == {}:
            self.actions = {K_z: "onZPress",K_x: "onXPress"}
        else:
            self.actions = actions

    def keyDownHandler(self,savegame,key):
        if key in self.actions.keys():
            savegame = getattr(self,self.actions[key])(savegame)
            return savegame
        return savegame

    def onZPress(self,savegame):
        savegame.room += 1
        return savegame

    def onXPress(self,savegame):
        savegame.room += 2
        return savegame

rooms = [BasicRoom("Welcome to Existance!","Welcome, {playername}, to Existance. Existance is a text adventure game where YOU are\nthe main character. Here is the story.\n\nOne day, {playername} was walking through town.\nWhen they passed by the TV shop, there was breaking news! Someone\nhad robbed the Fantasyville Central Bank and got away with everyone's\nmoney, so now, everyone was flat broke.\n\nBecause everyone was flat broke, stores that used to sell things gave\nthings away to people in need. Everyone sent food and the like to\nFantasyville after hearing about the sad state it was in.\n\nEveryone got by with what they had.\n\nIt was existance.\nIt was beauty.\n\nBut to some, including {playername}, it was boring.\nSo they decided to get to the root cause of their continued economic depression."),Act1Room("Investigation 1: Checking for clues","{playername} was eating lunch at Smiley's Good Eats. They narrowed\ndown the 2 best places to find clues: The bank, or the supposed robber's house.\n\nPress Z to check the bank, or X to check the robber's house."),EndRoom("Default End","This is the end."),EndRoom("Default End","This is the end.")]
