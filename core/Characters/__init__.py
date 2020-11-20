import random
import time
import base64
import json

import core.Errors as errs
from core.utils import ParserGet, ParserSetup
from core.utils.Colors import bcolors as css

random.seed(time.time())

class Player():
    def __init__(self, col, rows, engine):
        self.id=random.randint(10,100)
        self.pos=[random.randint(0,5),random.randint(0,4)]
        self.Engine=engine
        self.selected=None
        self.img='P'
    
    def move(self, pos):
        newx=int(pos.split(',')[0]); x=self.pos[0]
        newy=int(pos.split(',')[1]); y=self.pos[1]
        skip=None
        if x in [0,5]:
            if newx>x:
                if x==4:
                    skip='x'
            else:
                if x==0:
                    skip='x'
        if y in [0,4]:
            if newy>y:
                if y==3:
                    skip='y'
            else:
                if y==0:
                    skip='y'
        if not skip:
            for bot in self.Engine.robots:
                if bot.pos==[newx, newy]:
                    if not bot.id==self.id:
                        print(css.FAIL+'[ERR]'+css.ENDC+' ID:',bot.id,'already in',newx,',',newy,'!')
                    return
            self.pos=[newx, newy]
        else:
            if skip=='y':
                for bot in self.Engine.robots:
                    if bot.pos==[newx, y]:
                        if not bot.id==self.id:
                            print(css.FAIL+'[ERR]'+css.ENDC+' ID:',bot.id,'already in',newx,',',newy,'!')
                        return
                self.pos=[newx, y]
            else:
                for bot in self.Engine.robots:
                    if bot.pos==[x, newy]:
                        if not bot.id==self.id:
                            print(css.FAIL+'[ERR]'+css.ENDC+' ID:',bot.id,'already in',newx,',',newy,'!')
                        return
                self.pos=[x, newy]

class Kernel():
    def __init__(self):
        self.islocked=True
        self.is_active=True
        self.ports={'80':1, '443':1}
        self.hashes={}
        [self.hashes.update({port:base64.b64encode(''.join([chr(random.randint(97,122)) for _ in range(5)]).encode()).decode()}) for port in self.ports.keys()]

class Robot():
    def __init__(self, Engine):
        self.id=random.randint(10,100)
        self.pos=[random.randint(0,5),random.randint(0,4)]
        self.img='R'
        # --
        self.state=css.FAIL+'locked'+css.ENDC
        self.kernel=Kernel()
        self.Engine=Engine

    def parser(self, x):
        cmd=x.split()[0].lower()
        params=x.split()[1:]
        # TODO add parser
        if '-h' in params:
            self.docs(cmd)
            return
        
        # HELP
        if cmd=='help':
            return
        
        # SCAN
        elif cmd=='hack':
            port=str(params[params.index('-port')+1])
            if self.kernel.ports[port]==1:
                raise errs.HackError()
            else:
                print(css.OKCYAN+'[..]'+css.ENDC+' Hacking on port:',params[0])
                self.kernel.islocked=False
                self.state=css.OKGREEN+'unlocked'+css.ENDC
                time.sleep(0.5)
                print(css.OKCYAN+'[*]'+css.ENDC+css.OKGREEN+' Successfully hacked.'+css.ENDC)
        
        # SCAN
        elif cmd=='scan':
            print(css.OKCYAN+'[..]'+css.ENDC+' Scanning...')
            print('[*] Found ports:')
            for port in self.kernel.ports.keys():
                if self.kernel.ports[port] in ['1',1]:
                    print('-',css.HEADER+port,css.ENDC+' status:'+css.FAIL,self.kernel.ports[port],css.ENDC)
                else:
                    print('-',port,' status:'+css.OKGREEN,self.kernel.ports[port], css.ENDC)

        # SHUTDOWN
        elif cmd in ['destroy', 'shutdown']:
            if self.kernel.islocked: raise errs.HackError(css.OKCYAN+'\n[INFO]'+css.ENDC+' Unlock kernel first.'); return
            print(css.FAIL+'[..]'+css.ENDC+' Self-Destruction Enabled..')
            self.kernel.is_active=False
            self.Engine.robots.remove(self)
            time.sleep(0.4)
            self.Engine.gamepoints+=1
            print(css.HEADER+'[*]'+css.ENDC+' Bot killed.')

        # BSHELL
        elif cmd=='bshell':
            if self.kernel.islocked: raise errs.HackError(css.OKCYAN+'\n[INFO]'+css.ENDC+' Unlock kernel first.'); return
            if self.kernel.is_active: raise errs.HackError(css.OKCYAN+'\n[INFO]'+css.ENDC+' Disable kernel first.'); return
            print(css.OKGREEN+'[CMD]'+css.ENDC+' Entering BrainShell...')
            if self.level<=1:
                print(css.FAIL+'[ERR][#51]'+css.ENDC+' BShell unreacheable, this robot hasnt a BShell interface.')
            else:
                if len(params):
                    self.BShell(' '.join(params))
                else:
                    self.Engine.inbshell=True
        
        # INFO
        elif cmd=='info':
            [print(k,'->',self.kernel.__dict__[k]) for k in self.kernel.__dict__ if not k.startswith('__')]
        
    def BShell(self, x):
        raise NotImplementedError()

    def docs(self, man):
        data=json.loads(open('core/Characters/cmds.json').read())
        for key in data['cheatsheet'][man]:
            print(key,'->',data['cheatsheet'][man][key])
