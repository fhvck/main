import os, sys, random
import pygame
from pygame.locals import *
from xml.dom.minidom import parse

class MAP(object):
    def __init__(self, WindowManager, screen):
        self._screen = screen
        self._tiles={}
        self.map=[]
    
    def LoadTiles(self, arch):
        print('[*] Loading tiles...')
        tilesArch = parse(arch)
        tilesList = tilesArch.getElementsByTagName('azulejo')
        for tile in tilesList:
            self._tiles[tile.childNodes[0].nodeValue] = pygame.image.load(os.path.join('data', 'images', 'terrain', tile.childNodes[0].nodeValue+'.png'))
            self._tiles[tile.childNodes[0].nodeValue].convert()
    
    def MakeMap(self, arch, pos=0):
        print('[*] Building the world...')
        mapArch = parse(arch)
        MapLines = mapArch.getElementsByTagName('fila')
        for fila in MapLines:
            MapColumns = fila.getElementsByTagName('columna')
            filamapa=[]
            for column in MapColumns:
                filamapa.append(column.childNodes[0].nodeName)
            self.map.append(filamapa)
    
    def showMap(self, sprite=None):
        x=20; y=10
        startX = 0
        startY = 0
        posX = posY = 0
        scrollMapX = 0
        scrollMapY = 0
        #drawedWin = pygame.Surface([self._screen.get_width(), self._screen.get_height()])
        if sprite:
            scrollMapX = sprite.scrollMapX
            scrollMapY = sprite.scrollMapY
        for line in self.map[scrollMapY:]:
            posY += 1
            posX = -1
            if 380 - (posY*x)+(posX*x) < -20:
                break
            for tile in line[scrollMapX:]:
                posX += 1
                if not 380 - (posY * x) + (posX * x) > 760 - (posY * 19):
                    self._screen.blit(self._tiles[tile], (380 - (posY * x) + (posX * x), 180 + (posY * y) + (posX * y)))
                    if sprite:
                        if posX + scrollMapX == sprite.pos[0] and posY + scrollMapY == sprite.pos[1]:
                            self._screen.blit(sprite.spriteActual, (380 - (posY * x) + ((posX) * x), 180 + (posY * y) + ((posX) * y) - 20))