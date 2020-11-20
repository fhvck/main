import base64
import json
import os
import random
import sys
import time

import core.Errors as errs
from core.Characters import Player, Robot
from core.utils.Colors import bcolors as css
from core.PC import computer
from core.utils import *
from core.Shop import Shop

random.seed(time.time())

# load screens
# FIXME print non interpreta le sequenze di escape nei banner

points={
    "win":10,
    "kill":1
}

class Engine():
    def __init__(self, col=4, rows=5, enems=3):
        self.gamepoints=0
        # map setup
        self.columns=col
        self.rows=rows
        self.map=[['_' for _ in range(rows+1)] for _ in range(col+1)]
        # match maker setup
        self.robots=[Robot(self) for _ in range(enems)]
        self.player=Player(col, rows, self)
        self.robots.append(self.player)
        # external objs setup
        self.shop=Shop(self)
        # graphic settings
        self.showids=False
        self.showpos=False
        self.overrideshow=False
        self.inbshell=False
        self.inshop=False

    def run(self):
        while True:
            self.update_map()
            while self.inbshell:
                try:
                    self.selected.BShell(input(css.OKCYAN+'[CMD]'+css.ENDC+css.OKGREEN+'[BSH]'+css.ENDC+' >> '))
                except IndexError:
                    print(css.FAIL+'[ERR]'+css.ENDC+' Missing a parameter.')
                except Exception as e:
                    print(css.FAIL+'[ERR]'+css.ENDC,str(e))
            while self.inshop:
                try:
                    self.shop.run()
                except IndexError:
                    print(css.FAIL+'[ERR]'+css.ENDC+' Missing a parameter')
                except Exception as e:
                    print(css.FAIL+'[ERR]'+css.ENDC,str(e))
            try:
                if self.player.selected:
                    # Robot parser
                    self.player.selected.parser(input(css.OKGREEN+'[BOT]'+css.ENDC+css.OKCYAN+'[SCORE:{}]'.format(self.gamepoints)+css.ENDC+' -state:{}- >> '.format(self.player.selected.state)))
                else:
                    self.show_map()
                    self.parser(input('\n[MAP][SCORE:{}] >> '.format(self.gamepoints))) # map parser
            except errs.ParamError as e:
                print(str(e))
            except errs.SameObjError as e:
                print(str(e))
            except Exception as e:
                print(str(e)); continue
    
    def parser(self, x):
        cmd=x.split()[0].casefold()
        params=x.split()[1:]
        if '-h' in params:
            self.docs(cmd)
            return
        if cmd=='help':
            if not len(params):
                print(css.HEADER+'[*]'+css.ENDC+' List of commands:')
                [print(command) for command in json.loads(open('core/commands.json').read())['commands']]
            else:
                self.docs(params[0].casefold())
        elif cmd=='show':
            if '-a' in params:
                self.overrideshow=True
            if 'id' in params or '-id' in params:
                self.showids=True
                self.showpos=False
            elif 'pos' in params or '-pos' in params:
                self.showids=False
                self.showpos=True
            elif 'null' in params or '-null' in params:
                self.showids=False
                self.showpos=False
            else:
                raise errs.ParamError(params)
        elif cmd=='select':
            if '-id' in params:
                v=int(params[params.index('-id')+1])
                for bot in self.robots:
                    if bot.id==v:
                        if bot==self.player:
                            raise errs.SameObjError(bot, self.player)
                            return
                        self.player.selected=bot
            elif '-pos' in params:
                v=params[params.index('-pos')+1]
                for bot in self.robots:
                    if bot.pos==[int(i) for i in v.split(',')]:
                        self.player.selected=bot
            else:
                raise errs.ParamError(params)
        elif cmd=='move':
            self.player.move(params[0])
        elif cmd=='bye':
            print('[?] Are you sure?')
            c=getch()
            if c in ['y','s']:
                # accredita
                #globals()['srcdata']['score']+=self.gamepoints
                main()
            elif c=='n':
                return
            else:
                print(css.FAIL+'[ERR]'+css.ENDC+' Unrecognized key, back to game.')
        else:
            raise errs.CommandNotFoundError(cmd)
            #breakpoint()
    
    def update_map(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                pos=[x,y]; done=False
                for bot in self.robots:
                    if bot.pos==pos:
                        if bot.img=='P':
                            if self.overrideshow:
                                if self.showids:
                                    self.map[y][x]=bot.id; done=True
                                elif self.showpos:
                                    self.map[y][x]=','.join([str(p) for p in bot.pos]); done=True
                                else:
                                    self.map[y][x]=bot.img; done=True
                            else:
                                self.map[y][x]='U'; done=True
                        elif self.showids:
                            self.map[y][x]=bot.id; done=True
                        elif self.showpos:
                            self.map[y][x]=','.join([str(p) for p in bot.pos]); done=True
                        else:
                            self.map[y][x]=bot.img; done=True
                if not done:
                    self.map[y][x]='_'
        self.overrideshow=False
        return self.map
    
    def show_map(self):
        for y in self.map:
            for x in y:
                print(x, end=' ')
            print()
    
    def docs(self, man):
        data=json.loads(open('core/commands.json').read())
        for key in data['cheatsheet'][man]:
            print(key,'->',data['cheatsheet'][man][key])

def main(*oth):
    if not oth:
        print(" _____ _              _    \n|  ___| |____   _____| | __\n| |_  | '_ \\ \\ / / __| |/ /\n|  _| | | | \\ V / (__|   < \n|_|   |_| |_|\\_/ \\___|_|\\_\\\n                           \n")
    else:
        print(*oth)

    x=input('\n\n$[MAIN] ')
    cmd=x.split()[0].casefold()
    params=x.split()[1:]
    cls_()
    if cmd in ['.start','start']:
        game=Engine()
        game.run()

    elif cmd=='./mypc':
        print('getting into ur pc.')

    elif cmd in ['exit', 'bye']:
        print('[*] Exiting...')
        exit()

    else:
        main('[ERR] Unrecognized command:',cmd)

main()

