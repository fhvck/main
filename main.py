#!/usr/bin/env python

import os, sys

try:
    from xml.dom.minidom import parse
except ImportError:
    print( "Error: xml.dom.minidom module not found. Verify your python installation.")
    sys.exit(1)

try:
    import random
except ImportError:
    print( "Error: random module not found. Verify your python installation.")
    sys.exit(1)

try:
    import pygame
except ImportError:
    print( "Error: pygame module not installed. Install pygame module.") #TODO add autoinstaller
    sys.exit(1)

try:
    from pygame.locals import *
except ImportError:
    print ("Error: pygame.locals not found. Verify your pygame installation.")
    sys.exit(1)

from core.mapManager import MAP
from core.playerManager import PlayerManager
from core.defines import *
from core.defines import _blit_messages

# --------------------------------------------------------
# ---------------- M A I N  M E N U ----------------------
# --------------------------------------------------------

while True:
    # start menu screen
    pygame.event.pump()
    kin = pygame.key.get_pressed()
    screen.blit(background, (0,0))

    count+=1
    flag=False

    if count>=1 and count<300 and not contsprite==0:
        contsprite=0
        flag=True
    elif count>=300 and count<600 and not contsprite==1:
        contsprite=1
        flag=True
    elif count>=600 and count<900 and not contsprite==2:
        contsprite=2
        flag=True
    elif count>=900 and count<1200 and not contsprite==1:
        contsprite=1
        flag=True
    elif count==1200:
        count=0
    
    if flag:
        screen.blit(font, (window.centrarItemX(font), window.centrarItemY(font)))
        screen.blit(logo[contsprite], (window.centrarItemX(logo[contsprite]), window.centrarItemY(logo[contsprite])/2))
        pygame.display.update()
    
    # handle events
    if kin[K_RETURN]:
        break # break this loop and launch the game loop
    elif kin[K_ESCAPE] or pygame.event.peek(QUIT):
        sys.exit() # stop the code
pygame.time.delay(500)

# --------------------------------------------------------
# --------------------- G A M E --------------------------
# --------------------------------------------------------

while True:
    # game loop
    pygame.event.pump()
    kin = pygame.key.get_pressed()
    player.action(kin)
    screen.blit(background,(0,0))
    mappa.showMap(sprite=player)
    _blit_messages()
    pygame.display.flip()
    if player.hp<=0:
        break # if player life is under zero stop the loop #TODO add: enter the menuscreen loop

while True:
    break # this loop is the game over loop!

pygame.time.delay(500)
