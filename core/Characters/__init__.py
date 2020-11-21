import base64
import json
import random
import time
import xml.etree.ElementTree as ET

import core.Errors as errs
from core.utils import ParserGet, ParserSetup
from core.utils.Colors import bcolors as css

random.seed(time.time())

class Player():
    def __init__(self, col, rows, engine):
        self.id=random.randint(10,100)
        self.pos=[random.randint(0,4),random.randint(0,3)]
        self.Engine=engine
        self.selected=None
        self.img='P'
        self.action_range=1 # it means center+1, so 3*3 grid
    
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
                if newx<=self.pos[0]+self.action_range and newx>=self.pos[0]-self.action_range:
                    if newy<=self.pos[1]+self.action_range and newy>=self.pos[1]-self.action_range:
                        self.pos=[newx, newy]
                    else:
                        print(errs.ActionRangeError(pos=[newx,newy])); return
                else:
                    print(errs.ActionRangeError(pos=[newx,newy])); return
        else:
            if skip=='y':
                for bot in self.Engine.robots:
                    if bot.pos==[newx, y]:
                        if not bot.id==self.id:
                            print(css.FAIL+'[ERR]'+css.ENDC+' ID:',bot.id,'already in',newx,',',newy,'!')
                            return
                    # newpos=[newx, y]
                    if newx<=self.pos[0]+self.action_range and newx>=self.pos[0]-self.action_range:
                        if y<=self.pos[1]+self.action_range and y>=self.pos[1]-self.action_range:
                            self.pos=[newx, y]
                        else:
                            print(errs.ActionRangeError(pos=[newx, y])); return
                    else:
                        print(errs.ActionRangeError(pos=[newx, y])); return
            else:
                for bot in self.Engine.robots:
                    if bot.pos==[x, newy]:
                        if not bot.id==self.id:
                            print(css.FAIL+'[ERR]'+css.ENDC+' ID:',bot.id,'already in',newx,',',newy,'!')
                        return
                    if x<=self.pos[0]+self.action_range and x>=self.pos[0]-self.action_range:
                        if newy<=self.pos[1]+self.action_range and newy>=self.pos[1]-self.action_range:
                            self.pos=[x, newy]
                        else:
                            print(errs.ActionRangeError(pos=[x,newy])); return
                    else:
                        print(errs.ActionRangeError(pos=[x,newy])); return

class Kernel():
    def __init__(self):
        self.islocked=True
        self.is_active=True
        self.ports={'80':1, '443':1}
        self.hashes={}
        [self.hashes.update({port:base64.b64encode(''.join([chr(random.randint(97,122)) for _ in range(5)]).encode()).decode()}) for port in self.ports.keys()]

class Robot():
    def __init__(self, Engine, img='R'):
        self.id=random.randint(10,100)
        self.pos=[random.randint(0,5),random.randint(0,4)]
        self.img=css.FAIL+img+css.ENDC
        self.color=css.FAIL
        self.level=2
        # --
        self.commands=json.loads(open('core/Characters/commands.json').read())['commands']
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
            print(css.HEADER+'[H]'+css.ENDC+' List of commands:'); [print('-',cmd) for cmd in self.commands]
            print(css.HEADER+'[H]'+css.ENDC+' Type "cmd -h" for info about cmd.')
        
        # HACK
        elif cmd=='hack':
            port=str(params[params.index('-port')+1])
            if self.kernel.ports[port]==1:
                raise errs.HackError()
            else:
                print(css.OKCYAN+'[..]'+css.ENDC+' Hacking on port:',params[0])
                self.kernel.islocked=False
                self.state=css.OKGREEN+'unlocked'+css.ENDC
                self.img=css.OKGREEN+(self.img.replace(css.FAIL, ''))
                self.color=css.OKGREEN
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
            self.Engine.player.selected=None
            # dump the score
            tree=ET.parse('core/PC/config.xml')
            root=tree.getroot()
            for ch in root.iter('points'):
                ch.text=str(self.Engine.gamepoints)
            tree.write('core/PC/config.xml')

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
        
        # HASH
        elif cmd=='hash':
            if not len(params): params.append('-port')
            if params[0]=='-port':
                # show mode, mostra la cifratura della porta
                try:
                    print(css.OKCYAN+'[HASH]'+css.ENDC,params[1],self.kernel.hashes[str(params[1])])
                except Exception:
                    [print(css.OKCYAN+'[HASH]'+css.ENDC,key,self.kernel.hashes[key]) for key in self.kernel.hashes.keys()]
            elif params[0]=='-res':
                # map commands like: {param:val}
                mappedparams={}
                for p in params:
                    if not p.startswith('-'): continue
                    try:
                        mappedparams.update({p:params[params.index(p)+1]})
                    except: break
                if mappedparams['-res']==base64.b64decode(self.kernel.hashes[mappedparams['-port']]).decode():
                    self.kernel.ports[mappedparams['-port']]=0
                    print(css.HEADER+'[*]'+css.ENDC+' Port {p} Successfully bypassed.'.format(p=mappedparams['-port']))
                else:
                    print(css.FAIL+'[!!] Failed.'+css.ENDC)
            else:
                print(css.WARNING+'[WARN]'+' Unrecognized param {p}, using "-port" instead.'.format(p=params[0]))
                try:
                    print(css.OKGREEN+'[HASH]'+css.ENDC,params[1],self.kernel.hashes[str(params[1])])
                except Exception:
                    [print(css.OKGREEN+'[HASH]'+css.ENDC,key,self.kernel.hashes[key]) for key in self.kernel.hashes.keys()]
        
        # TRANSLATER
        elif cmd in ['translater', 'encoder', 'decoder']:
            if cmd=='encoder':
                s=params[params.index('-text')+1]
                print(css.HEADER+'[*]'+css.ENDC+' Encoded text: '+css.OKBLUE, base64.b64encode(s).decode(),css.ENDC)
            elif cmd=='decoder':
                s=params[params.index('-text')+1]
                print(css.HEADER+'[*]'+css.ENDC+' Decoded text: '+css.OKBLUE, base64.b64decode(s).decode(),css.ENDC)
            elif cmd=='translater':
                if not '-mode' in params:
                    if 'encode' in params or 'decode' in params:
                        if 'encode' in params:
                            s=params[params.index('-text')+1]
                            print(css.HEADER+'[*]'+css.ENDC+' Encoded text: ', base64.b64encode(s).decode())
                        else:
                            s=params[params.index('-text')+1]
                            print(css.HEADER+'[*]'+css.ENDC+' Decoded text: ', base64.b64decode(s).decode())
        
        # EXIT
        elif cmd in ['exit', 'bye']:
            print('exiting')
            self.Engine.player.selected=None

    
    def BShell(self, x):
        raise NotImplementedError()

    def docs(self, man):
        data=json.loads(open('core/Characters/cmds.json').read())
        for key in data['cheatsheet'][man]:
            print(key,'->',data['cheatsheet'][man][key])
