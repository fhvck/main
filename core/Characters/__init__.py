import base64
import json
import random
import time
import xml.etree.ElementTree as ET
from functools import reduce

import core.Errors as errs
from core.utils import list_splice
from core.utils.Colors import bcolors as css

random.seed(time.time())

tips=[
    "one number is correct and well placed",
    "nothing is correct",
    'two numbers are correct but wrong placed',
    'one number is correct but wrong placed',
    'one number is correct but wrong placed'
]

sequences=[[], [], [], [], []]

numbers=[i for i in range(0,10)]

def shuffle(matrix):
    for i in range(0, len(matrix)-1):
        j=int(random.random()*(i+1))
        x=matrix[i]
        matrix[i]=matrix[j]
        matrix[j]=x
    return matrix

def spliceRandNumber(array=None):
    if not array:
        array=numbers
    return (list_splice(array,int(random.random()*len(array)), 1))[0]

def newCode():
    global sequences
    global numbers
    code=[None,None,None]
    sequences=[[], [], [], [], []]
    numbers=[i for i in range(0,10)]
    codeNumbers=[spliceRandNumber() for _ in range(3)]

    sequences[0] = [codeNumbers[0], spliceRandNumber(), spliceRandNumber()]
    sequences[1] = [sequences[0][1], spliceRandNumber(), spliceRandNumber()]
    sequences[2] = [codeNumbers[1], codeNumbers[2], sequences[1][1]]
    sequences[3] = [codeNumbers[0], sequences[1][2], spliceRandNumber()]
    fifthSequenceNId = int(random.random()*2)+1
    sequences[4] = [codeNumbers[fifthSequenceNId], spliceRandNumber(), spliceRandNumber()]

    for s in sequences:
        s=shuffle(s)

    places = [sequences[0].index(codeNumbers[0]),None,None]
    
    code[places[0]] = codeNumbers[0]
    
    for i in range(0,3):
        if not code[i]:
            if not codeNumbers[1] in code: # code.index(codeNumbers[1]) < 0:
                code[i] = codeNumbers[1]
                places[1]=i
            else:
                code[i] = codeNumbers[2]
                places[2]=i

    fixThirdSequence(codeNumbers, places)
    fixFourthSequence(codeNumbers, places)
    fixFifthSequence(fifthSequenceNId, codeNumbers, places)

    i=0
    for s in sequences:
        print(s, tips[i])
        i+=1
    
    return code

#adjust last sequences
def fixThirdSequence(codeNumbers, places):
    global sequences
    index1=sequences[2].index(codeNumbers[1])
    index2=sequences[2].index(codeNumbers[2])
    if not index1==places[1] and not index2==places[2]: return
    sequences[2][index1] = codeNumbers[2]
    sequences[2][index2] = codeNumbers[1]

def fixFourthSequence(codeNumbers,places):
    global sequences
    index=sequences[3].index(codeNumbers[0])
    for i in range(0,3):
        if not sequences[3][i]==codeNumbers[0] and sequences[3][i] in sequences[3]:
            sequences[3][i]=random.choice(sequences[1])
    if not index==places[0]: return
    if index>1:
        change=sequences[3][index-1]
        sequences[3][index - 1] = codeNumbers[0]
        sequences[3][index] = change
    else:
        change = sequences[3][index + 1]
        sequences[3][index + 1] = codeNumbers[0]
        sequences[3][index] = change

def fixFifthSequence(nId, codeNumbers, places):
    index=sequences[4].index(codeNumbers[nId])
    seqTwoIndex = sequences[2].index(codeNumbers[nId])
    if (index==places[nId] or type(index)==type(places[nId])) or (seqTwoIndex==index or type(seqTwoIndex)==type(index)):
        newIndex= reduce(lambda acc, cur: acc+([cur if not cur==seqTwoIndex and not cur==places[nId] else 0][0]), [0,1,2], 0)
        change= sequences[4][newIndex]
        sequences[4][newIndex] = codeNumbers[nId]
        sequences[4][index]= change


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
        
        # CRACK
        # TODO aggiungi che se non è comprato non si esegue!! (controlla i file json per vedere se comprato)
        elif cmd=='crack':
            if '-port' in params:
                p=params[params.index('-port')+1]
            else:
                p=params[0]
            if self.kernel.islocked: raise errs.HackError(css.OKCYAN+'\n[INFO]'+css.ENDC+' Unlock kernel first.'); return
            if not self.kernel.is_active: raise errs.HackError(css.OKCYAN+'\n[INFO]'+css.ENDC+' Kernel already disabled.'); return
            # resolve pattern
            print(css.HEADER+'[PATTERN]'+css.ENDC+' Resolve:')
            code=newCode()
            print(css.OKCYAN+'[INFO]'+css.ENDC+' Code: XXX')
            rep=input(css.OKBLUE+'[SOLUTION]'+css.ENDC+' >> ')
            if rep==''.join([str(i) for i in code]):
                self.kernel.is_active=False
                print(css.OKGREEN+'[OK]'+css.ENDC+css.OKCYAN+' Kernel Successfully disabled!'+css.ENDC)
            else:
                print(css.FAIL+'[ERR]'+css.ENDC+' Verification Failed.')
        
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
        
        # EXIT
        elif cmd in ['exit', 'bye']:
            print('exiting')
            self.Engine.player.selected=None

    
    def BShell(self, x=None):
        comms=json.loads(open('core/Characters/commands.json').read())['bscommands']
        cmd=x.split()[0].lower()
        params=x.split()[1:]
        if '-h' in params: self.BSHdocs(cmd); return
        if not cmd in comms:
            if cmd=='bshell' or not cmd:
                # start a serial communication
                self.Engine.inbshell=True
                if params[0] in comms:
                    cmd=params[0]
                    params.remove(params[0])
                else: return
            else:
                print(css.FAIL+'[ERR]'+css.ENDC+' Unrecognized command:', cmd)
                return
        # exec live commands

        # MOVE
        if cmd=='move':
            if '-pos' in params:
                self.move(params[params.index('-pos')+1])
            else:
                self.move(params[0])
        
        # ATTACK
        elif cmd in ['atk', 'attack']:
            if '-h' in params:
                self.BSHdocs(cmd)
            bot=None
            #if not '-pos' in params: and not '-id' in params:
            #    print(css.FAIL+'[ERR]'+css.ENDC+' Invalid syntax, check "atk -h" for help.'); return
            #if self.selected and not '-bot' in params:
                #bot=self.selected
            #if not '-bot' in params:
                # find the bot
                # default method = id
            if not '-pos' in params: # if doesnt override selecting mode
                for obj in self.Engine.robots:
                    try:
                        if str(obj.id)==str(params[params.index('-id')+1]):
                            bot=obj; break
                    except:
                        if str(obj.id)==str(params[0]):
                            bot=obj; break
                if not bot:
                    print(css.FAIL+'[ERR]'+css.ENDC+' Invalid id.')
                    return
            else:
                # use position
                for obj in self.Engine.robots:
                    if str(obj.pos)==str(params[params.index('-pos')+1]):
                        bot=obj; break
                if not bot:
                    print(css.FAIL+'[ERR]'+css.ENDC+' Invalid position.')
            if not self.inrange(bot): print(css.FAIL+'[ERR][#78]'+css.ENDC+' Bot unreachable, too far.'); return
            print('[*] Decoded hashes:')
            if not '-port' in params:
                [print('- port',port,'\b:',base64.b64decode(bot.kernel.hashes[port]).decode()) for port in bot.kernel.hashes.keys()]
            else:
                print('- port',port,'\b:',base64.b64decode(bot.kernel.hashes[params[params.index('-port')+1]]).decode())
        
        # RETRIEVE
        elif cmd=='retrieve':
            # qualsiasi pos va bene
            if not '-pos' in params: # if doesnt override selecting mode
                for obj in self.Engine.robots:
                    if str(obj.id)==str(params[params.index('-id')+1]):
                            bot=obj; break
                if not bot:
                    print(css.FAIL+'[ERR]'+css.ENDC+' Invalid id.')
            else:
                # use position
                for obj in self.Engine.robots:
                    if str(obj.pos)==str(params[params.index('-pos')+1]):
                        bot=obj; break
            if not bot:
                print(css.FAIL+'[ERR]'+css.ENDC+' Invalid position.')
            print('[*] Retrieved data:')
            [print('[BOTDATA]',k,'->',bot.__dict__[k]) for k in bot.__dict__ if not k.startswith('__')]
            print()
            [print('[KERNEL]',k,'->',bot.kernel.__dict__[k]) for k in bot.kernel.__dict__ if not k.startswith('__')]
        
        # DMG && FIRE
        elif cmd in ['dmg', 'fire']:
            if not '-pos' in params: # if doesnt override selecting mode
                for obj in self.Engine.robots:
                    if str(obj.id)==str(params[params.index('-id')+1]):
                            bot=obj; break
                if not bot:
                    print(css.FAIL+'[ERR]'+css.ENDC+' Invalid id.')
            else:
                # use position
                for obj in self.Engine.robots:
                    if str(obj.pos)==str(params[params.index('-pos')+1]):
                        bot=obj; break
            if not bot:
                print(css.FAIL+'[ERR]'+css.ENDC+' Invalid position.')
            if bot.kernel.islocked: raise errs.HackError(css.OKCYAN+'\n[INFO]'+css.ENDC+' Unlock kernel first.'); return
            print(css.FAIL+'[..]'+css.ENDC+' Self-Destruction Enabled..')
            bot.kernel.is_active=False
            self.Engine.robots.remove(bot)
            time.sleep(0.4)
            self.Engine.gamepoints+=1
            print(css.HEADER+'[*]'+css.ENDC+' Bot killed.')
        
        # REMOTEHACK
        elif cmd in ['remotehack', 'rmh']:
            bot=None
            if not '-pos' in params: # if doesnt override selecting mode
                for obj in self.Engine.robots:
                    try:
                        if str(obj.id)==str(params[params.index('-id')+1]):
                            bot=obj; break
                    except:
                        if str(obj.id)==str(params[0]):
                            bot=obj; break
                if not bot:
                    print(css.FAIL+'[ERR]'+css.ENDC+' Invalid id.')
            else:
                # use position
                for obj in self.Engine.robots:
                    if str(obj.pos)==str(params[params.index('-pos')+1]):
                        bot=obj; break
            if not bot:
                print(css.FAIL+'[ERR]'+css.ENDC+' Invalid position.'); return
            print(css.OKCYAN+'[..]'+css.ENDC+' Hacking bot',bot.id)
            bot.kernel.islocked=False
            bot.state=css.OKGREEN+'unlocked'+css.ENDC
            time.sleep(0.5)
            print(css.OKCYAN+'[*]'+css.ENDC+css.OKGREEN+' Successfully hacked.'+css.ENDC)
        
        # EXIT
        elif cmd in ['bye', 'exit']:
            self.Engine.inbshell=False

        # HELP
        elif cmd=='help':
            print(css.HEADER+'[H]'+css.ENDC+' List of commands:'); [print('-',cmd) for cmd in comms]
            print(css.HEADER+'[H]'+css.ENDC+' Type "cmd -h" for info about cmd.')
        
        # MAP
        elif cmd=='map':
            if not len(params):
                md='std'
            else:
                if '-mode' in params:
                    md=params[params.index('-mode')+1]
                elif '-m' in params:
                    md=params[params.index('-m')+1]
                else:
                    md=params[0]
            if md in ['std', 'default', 'rapid', 'rmap']:
                # rapid map
                for bot in self.Engine.robots:
                    if bot.id==self.id: continue
                    try:
                        print('- bot'+css.OKBLUE,bot.id,css.ENDC+'at'+css.OKBLUE,bot.pos,css.ENDC+'state:'+bot.state)
                    except: continue # is player
            elif md in ['org', 'orig', 'original', 'general', 'main']:
                # main map
                if '-set' in params:
                    var=params[params.index('-set')+1]; val=params[params.index('-set')+2]
                    print(var,val)
                    if var in ['showids','showpos']:
                        exec('self.Engine.'+var+'='+str(bool(val)))
                self.Engine.show_map(self.Engine.update_map())
            else:
                print(css.FAIL+'[ERR]'+css.ENDC+' Unknown mode:', md)
                return

    def BSHdocs(self, man):
        data=json.loads(open('core/Characters/commands.json').read())
        for key in data['BSSheet'][man]:
            print(key,'->',data['BSSheet'][man][key])    

    def docs(self, man):
        data=json.loads(open('core/Characters/commands.json').read())
        for key in data['cheatsheet'][man]:
            print(key,'->',data['cheatsheet'][man][key])
