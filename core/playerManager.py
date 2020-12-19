import os, sys, random
import pygame
from pygame.locals import *

#FIXME spawn coordinates

COLOR_BLACK = 0
COLOR_BLUE = 1
COLOR_CYAN = 2
COLOR_GREEN = 3
COLOR_MAGENTA = 4
COLOR_RED = 5
COLOR_WHITE = 6
COLOR_YELLOW = 7
COLOR_BOLD = 8

class Player(pygame.sprite.Sprite):
    def __init__(self, _map, x, y, ancho, alto, spriteArch):
        super().__init__()
        self.map=_map
        self.spriteIndex = 0
        self.spriteActual = pygame.Surface([ancho, alto])
        self.initial = [x, y]
        self.pos=[x, y]
        self.hp=100
        self.speed=10
        self.acdist=10
        self.walkingmen = []
        sprites = pygame.image.load(os.path.join('data', 'images', 'character', 'body', spriteArch[0])).convert()
        sprites.set_colorkey(sprites.get_at((0,0)), RLEACCEL)
        spritesAncho, spritesAlto = sprites.get_size()
        for i in range(int(spritesAlto/alto)):
            self.walkingmen.append([])
            for j in range(int(spritesAncho/ancho)):
                self.walkingmen[i].append(sprites.subsurface(j*ancho, i*alto, ancho, alto))
        sprites = pygame.image.load(os.path.join('data', 'images', 'character', 'body', spriteArch[1])).convert()
        sprites.set_colorkey(sprites.get_at((0,0)), RLEACCEL)
        spritesAncho, spritesAlto = sprites.get_size()
        self.personajeGolpeando = []
        for i in range(int(spritesAlto/alto)):
            self.personajeGolpeando.append([])
            for j in range(int(spritesAncho/ancho)):
                self.personajeGolpeando[i].append(sprites.subsurface(j * ancho, i * alto, ancho, alto))
        self.personaje = self.walkingmen
        self.sprite=self.personaje[0][1]
        self.spriteActual=self.sprite
        self.rect = self.spriteActual.get_rect()
        # TODO add moving sprites, so direction too
    
    def mover(self, direction):
        incX = incY = 1
        if direction == 1:
            #TODO use self.dir (or //.direction come te pare) to update self.spriteActual
            if self.pos[1]>0:
                incY = -1
                incX = 0
        elif direction == 2:
            if self.pos[1]<len([fila[self.pos[0]] for fila in self.map.map])-1:
                incY = 1
                incX = 0
        elif direction == 3:
            if self.pos[0]>0:
                incY = 0
                incX = -1
        elif direction == 4:
            if self.pos[0] < len(self.map.map[self.pos[1]])-1:
                incY = 0
                incX = 1
        if incX != 0 or incY != 0: variabilechenoncapisco=0
        # TODO add: checka se puoi usare il prossimo tile
        self.pos[0]+=incX
        self.pos[1]+=incY
    
    def action(self, k):
        return k


class PlayerManager(Player):
    def __init__(self, _map, x, y, ancho, alto):
        super().__init__(_map, x-1, y, ancho, alto, ['drackoCaminar.bmp', 'drackoGolpear.bmp'])
        self.scrollMapX=0
        self.scrollMapY=0
        self.message=[]
    
    def mover(self, direction):
        self.add_message('moving')
        if direction == 1:
            if self.pos[1]>0: #TODO add blocked tiles
                if (len([fila[self.pos[0]] for fila in self.map.map]) - self.pos[1])-1>16 and self.scrollMapY>0:
                    self.scrollMapY -= 1
        elif direction == 2:
            if self.pos[1] < len([fila[self.pos[0]] for fila in self.map.map])-1:
                if self.pos[1] > 15 and len([fila[self.pos[0]] for fila in self.map.map]) - self.pos[1] > 4 and len([fila[self.pos[0]] for fila in self.map.map][self.scrollMapY:]) > 20:
                    self.scrollMapY += 1
        elif direction == 3:
            if self.pos[0]>0:
                if len(self.map.map[self.pos[1]]) - self.pos[0] > 16 and self.scrollMapX>0:
                    self.scrollMapX -= 1
        elif direction == 4:
            if self.pos[0] < len(self.map.map[self.pos[1]]) -1:
               if self.pos[0] > 15 and len(self.map.map[self.pos[1]]) - self.pos[0] >= 4 and len(self.map.map[self.pos[1]][self.scrollMapX:]) > 20:
                   self.scrollMapX+=1
        super(PlayerManager, self).mover(direction)
    
    def action(self, k):
        if self.acdist >= self.speed:
            self.acdist = 0
        else:
            self.acdist += 1
            return
        if self != None: # TODO add life points check
            if k[K_UP] or k[K_w]:
                self.mover(3)
            elif k[K_DOWN] or k[K_s]:
                self.mover(4)
            elif k[K_LEFT] or k[K_a]:
                self.mover(2)
            elif k[K_RIGHT] or k[K_d]:
                self.mover(1)
            # TODO add gameplay
    
    def add_message(self, message, color=6):
        l = []
        elt = ""
        for word in message.split(' '):
            if len(elt) + len(word) < 30:
                elt += " " + word
            else:
                l.append(elt[1:])
                elt = " " + word
        l.append(elt[1:])
        for mess in l:
            self.message.insert(0, (mess, color))
            if len(self.message) > 100:
                self.message.pop()