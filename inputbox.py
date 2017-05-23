# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return (event.key,True)
    elif event.type == KEYUP:
      return (event.key,False)
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  shift = False
  display_box(screen, question + ": " + string.join(current_string,""))
  while 1:
    inkey = get_key()
    if inkey[1]:
      inkey = inkey[0]
      if inkey == K_BACKSPACE:
        current_string = current_string[0:-1]
      elif inkey == K_RETURN:
        break
      elif inkey in (K_LSHIFT,K_RSHIFT):
        shift = True
      elif inkey <= 127:
        if shift:
          current_string.append(chr(inkey).upper())
        else:
          current_string.append(chr(inkey))
    else:
      if inkey[0] in (K_LSHIFT,K_RSHIFT):
        shift = False
    display_box(screen, question + ": " + string.join(current_string,""))
  return string.join(current_string,"")
