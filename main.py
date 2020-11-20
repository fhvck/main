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
    def __init__(self, col=4, rows=5, enems=1):
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
            if not len(self.robots) or (len(self.robots)==1 and self.robots[0]==self.player):
                self.win()
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
                    self.parser(input(css.OKGREEN+'[MAP]'+css.ENDC+css.OKCYAN+'[SCORE:{}]'.format(self.gamepoints)+css.ENDC+' >> ')) # map parser
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

        # HELP
        if cmd=='help':
            if not len(params):
                print(css.HEADER+'[*]'+css.ENDC+' List of commands:')
                [print(command) for command in json.loads(open('core/commands.json').read())['commands']]
            else:
                self.docs(params[0].casefold())
        
        # SHOW
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

        # SELECT
        elif cmd=='select':
            if '-id' in params:
                v=int(params[params.index('-id')+1])
                for bot in self.robots:
                    if bot.id==v:
                        if bot==self.player:
                            raise errs.SameObjError(bot, self.player)
                            return
                        if int(bot.pos[0])>=(int(self.player.pos[0])-self.player.action_range) and int(bot.pos[0])<=(int(self.player.pos[0])+self.player.action_range):
                            if int(bot.pos[1])>=(int(self.player.pos[1])-self.player.action_range) and int(bot.pos[1])<=(int(self.player.pos[1])+self.player.action_range):
                                self.player.selected=bot
                            else:
                                raise errs.ActionRangeError(bot)
                        else:
                            raise errs.ActionRangeError(bot)
            elif '-pos' in params:
                v=params[params.index('-pos')+1]
                for bot in self.robots:
                    if bot.pos==[int(i) for i in v.split(',')]:
                        if int(bot.pos[0])>=(int(self.player.pos[0])-self.player.action_range) and int(bot.pos[0])<=(int(self.player.pos[0])+self.player.action_range):
                            if int(bot.pos[1])>=(int(self.player.pos[1])-self.player.action_range) and int(bot.pos[1])<=(int(self.player.pos[1])+self.player.action_range):
                                self.player.selected=bot
                            else:
                                raise errs.ActionRangeError(bot)
                        else:
                            raise errs.ActionRangeError(bot)
            else:
                raise errs.ParamError(params)

        # MOVE
        elif cmd=='move':
            self.player.move(params[0])
        
        # EXIT && BYE
        elif cmd in ['bye', 'exit']:
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
    
    def win(self):
        self.gamepoints+=10
        cls_()
        titles=[
            '__   _____  _   _  __        _____ _   _ \n\\ \\ / / _ \\| | | | \\ \\      / /_ _| \\ | |\n \\ V / | | | | | |  \\ \\ /\\ / / | ||  \\| |\n  | || |_| | |_| |   \\ V  V /  | || |\\  |\n  |_| \\___/ \\___/     \\_/\\_/  |___|_| \\_|\n                                         \n',
            '                                                \n# #      #      # #         # #     ###     ### \n# #     # #     # #         # #      #      # # \n #      # #     # #         ###      #      # # \n #      # #     # #         ###      #      # # \n #       #      ###         # #     ###     # # \n'
            ]
        # TODO dump data
        print(css.OKGREEN+random.choice(titles)+css.ENDC)
        while True:
            print('Do you want to start a new game? (y\\n)')
            r=getch()
            if r.lower()=='y':
                main()
            elif r.lower()=='n':
                print('Exiting...')
                time.sleep(1); exit(code=0)
            else:
                print('[ERR] Invalid Key',r,'.')
                continue

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
                                self.map[y][x]=css.OKBLUE+'U'+css.ENDC; done=True
                        elif self.showids:
                            self.map[y][x]=bot.color+str(bot.id)+css.ENDC; done=True
                        elif self.showpos:
                            self.map[y][x]=','.join([str(p) for p in bot.pos]); done=True # TODO color here 
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

