import pygame,colors,save,os
from pygame.locals import *
import os.path as fs

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

pygame.init()
screen = pygame.display.set_mode((600,480))
pygame.display.set_caption("Existance")

logo_font = pygame.font.SysFont("Comic Sans MS",72)
logo = logo_font.render("Existance",True,colors.getColor("black"))

menu_font = pygame.font.SysFont("Comic Sans MS",36)
new_game_text = menu_font.render("New Game",True,colors.getColor("red"))
continue_text = menu_font.render("Continue",True,colors.getColor("red"))
new_game_rect = new_game_text.get_rect().move(20,106)
continue_rect = continue_text.get_rect().move(20,156)

main_font = pygame.font.SysFont("Arial",18)

menu = 0

def mainMenu():
    screen.blit(logo,(20,20))
    screen.blit(new_game_text,(20,106))
    if fs.exists("save.txt"):
        screen.blit(continue_text,(20,156))

def mainMenuCallback(e):
    global menu,savegame
    if e.type == MOUSEBUTTONDOWN:
        pos = list(pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[0] and new_game_rect.collidepoint(pos):
            savegame = save.SaveGame("save.txt",screen,True)
            print "[DEBUG] New game"
            menu += 1
        elif pygame.mouse.get_pressed()[0] and continue_rect.collidepoint(pos):
            savegame = save.SaveGame("save.txt",screen,False)
            print "[DEBUG] Continue"
            menu += 1
        if menu == 1:
            print "[DEBUG] Beginning in room "+str(savegame.room)

def prnt(text,x=0,y=0,c=colors.getColor("black")):
    drawText(screen,text,c,main_font.render(text,True,c).get_rect().move(x,y),main_font,True)

endrooms = (1,)

def room():
    global savegame
    if savegame.room == 0:
        prnt("Welcome to Existance, a choose-your-own-adventure game for players like you.",2,2)
    elif savegame.room == 1:
        prnt("This is the end.",2,2)

def roomCallback(e):
    global savegame,menu,endrooms
    if e.type == KEYDOWN and e.key == K_RETURN:
        if savegame.room in endrooms:
            menu = 0
            os.remove("save.txt")
            print "[DEBUG] End reached, save wiped, restarting from main menu."
            return
        savegame.room += 1
        print "[DEBUG] Going to room "+str(savegame.room)
        savegame.save()

running = True

while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            running = False
        if menu == 0:
            mainMenuCallback(e)
        elif menu == 1:
            roomCallback(e)
    if running:
        screen.fill(colors.getColor("white"))
        if menu == 0:
            mainMenu()
        elif menu == 1:
            room()
        pygame.display.flip()
exit(0)
