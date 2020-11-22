import json
import random
import time
import xml.etree.ElementTree as ET

from core.utils import cls_
from core.utils.Colors import bcolors as css

random.seed(time.time())

username=''

class Recognitor():
    def __init__(self, name:str, spec=None):
        self.spec=spec
        self.name=name.capitalize()
    
    def view_xml(self):
        tree=ET.parse('core/Recognition/botdata/bot.xml')
        root=tree.getroot()
        for ch in root:
            print(css.HEADER+'['+css.ENDC+'DATA'+css.HEADER+']'+css.ENDC,ch.tag,':')
            [print(subch.tag, subch.attrib, subch.text, sep=' -> ') for subch in ch]
            print()
    
    def render(self):
        self.view_xml()
    
    def call(self, player):
        print('Ciao ',username,'io sono',self.name+'. Sono felice di rivederti, ecco cosa ho scoperto in tua assenza.')
        tree=ET.parse('core/Recognition/botdata/bot.xml')
        root=tree.getroot()
        for ch in root:
            if ch.tag==self.spec:
                for subch in ch:
                    print(subch.tag,', w/',subch.attrib,' -> ',subch.text)


class Hendrix(Recognitor):
    def __init__(self):
        super().__init__('hendrix', spec='kernel')
    
    def creds(self):
        print('ciao, io sono Hendrix e sono uno specialista nei sistemi di attacco.')
        print('è merito mio se quei robot non possono attaccarci, ma ne stanno costruendo')
        print('di più potenti e il mio lock non potrà supportarli tutti, speriamo andrò tutto bene!')
        print('scrivi "call hendrix" per chiamarmi, rispondo sempre!')

class Alex(Recognitor):
    def __init__(self):
        super().__init__('alex', spec='comms')
    
    def creds(self):
        print('io sono Alex, un ricognitore specialista delle comunicazioni.')
        print('sto studiando da tempo le porte che permettono ai Robot di')
        print('interfacciarsi con i propri sistemi di sicurezza e con altri Robot.')
        print('scrivi "call alex" per chiamarmi, rispondo sempre!')


class RecoSquad():
    def __init__(self, Engine):
        global username
        username=ET.parse('core/PC/config.xml').getroot()[1][0].text
        self.squad={
            "Hendrix":Hendrix(),
            "Alex":Alex(),
            "You":Recognitor(username)
        }
        self.eng=Engine
    
    def parser(self, x:str, player):
        if not len(x):
            cls_()
            self.show_banner()
            self.eng.inreco=True
            return
        cmd=x.split()[0].casefold()
        params=x.split()[1:]
        if cmd=='call':
            if 'hendrix' in x.casefold().split()[1:]:
                self.squad['Hendrix'].call(player)
            elif 'alex' in x.casefold().split()[1:]:
                self.squad['Alex'].call(player)
        elif cmd in ['hendrix', 'alex']:
            self.squad[cmd.capitalize()].creds()
        else:
            print(css.FAIL+'[ERR]'+css.ENDC+' Unrecognized command:',cmd)
    
    def show_banner(self):
        print(random.choice(["               _           \n _ __ ___  ___| |__   ___  \n| '__/ _ \\/ __| '_ \\ / _ \\ \n| | |  __/ (__| | | | (_) |\n|_|  \\___|\\___|_| |_|\\___/ \n                           \n"]))
