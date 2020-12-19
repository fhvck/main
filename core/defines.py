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

# --------------------------------------------------------
# ------------------ D E F I N E S -----------------------
# --------------------------------------------------------

PYGAME_COLOR = ((0, 0, 0),
                (0, 127, 255),
                (99, 175, 255),
                (51, 155, 0),
                (255, 190, 255),
                (230, 146, 150),
                (255, 255, 255),
                (252, 235, 95),
                (0, 0, 0),
                (0, 127, 255),
                (99, 175, 255),
                (51, 155, 0),
                (255, 190, 255),
                (230, 146, 150),
                (255, 255, 255),
                (252, 235, 95))

COLOR_BLACK = 0
COLOR_BLUE = 1
COLOR_CYAN = 2
COLOR_GREEN = 3
COLOR_MAGENTA = 4
COLOR_RED = 5
COLOR_WHITE = 6
COLOR_YELLOW = 7
COLOR_BOLD = 8

FONT_SIZE = 5
SCREEN_SIZE = (1050, 600)

class WindowManager(object):
    def __init__(self, win):
        self._win = win
    
    def centrarItemX(self, item):
        screenX = 800#self._win.get_width() #logo screen is not 1044 but 800
        itemX = item.get_width()
        return (screenX/2)-(itemX/2)
    
    def centrarItemY(self, item):
        screenY = self._win.get_width() #logo height is always 600
        itemY = item.get_width()
        return (screenY/2)-(itemY/2)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
window=WindowManager(screen)

background=pygame.image.load('data/images/background/fondoNoche.png')

font=pygame.font.SysFont('Courier New', 15)
font = font.render('Press Enter to continue or Esc to Exit.', 1, (255,255,255))

logo = [
    pygame.image.load(
        'data/logo/titleLessOne.png'
    ), pygame.image.load(
        'data/logo/titleLessTwo.png'
    ), pygame.image.load(
        'data/logo/titleLessThree.png'
    ), 
]

panel = pygame.image.load(os.path.join("data", 'gui', "SidePanel.png"))
btfont = pygame.font.Font(os.path.join("data", 'gui', 
                                        "LiberationMono-Bold.ttf"), 
                                        FONT_SIZE+12)

screen.blit(panel, (1024-224, 0))

count=0
contsprite=0

def _blit_messages():
        """
        Blits player messages to the screen
        """
        global screen
        nb = min((SCREEN_SIZE[1] - 320) / FONT_SIZE, len(player.message))
        nb=int(nb)
        for i in range(nb):
            col_mess = player.message[nb-i-1][1]
            if col_mess > 7:
                shift = 2
            else:
                shift = 1
            screen.blit(BorderText(btfont, player.message[nb-i-1][0],
                              PYGAME_COLOR[col_mess], shift), 
                              (SCREEN_SIZE[0]-250+5, 290 + i * FONT_SIZE*3))

# define map and player (im calling map as "mappa" cuz map is a python built-in func :) )
tiles=open(os.path.join('data', 'maps', 'azulejos.xml'))
mapfile = open(os.path.join('data', 'maps', 'demo.xml'))
mappa = MAP(window, screen)
mappa.LoadTiles(tiles)
mappa.MakeMap(mapfile)
print('[*] Game successfully created!')
# make the player object
player=PlayerManager(mappa, 0, 0, 40, 40)

def BorderText(font, text, coul, shift=1):
    """
    Return a surface of white text with black border
    """
    coul_text = (0, 0, 0)
    surf_name = font.render(text, True, coul_text)
    surf = pygame.Surface((surf_name.get_width() + 2 * shift + 1, 
                           surf_name.get_height() + 2 * shift + 1), 
                           pygame.SRCALPHA, 32)
    #if shift >= 0:
    #    for i in range(0, 2 * shift + 1):
    #        for j in range(0, 2 * shift + 1):
    #            surf.blit(surf_name, (i, j))

    surf.blit(surf_name, (shift, shift))
    return surf
