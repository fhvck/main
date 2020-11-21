import random
import time
import xml.etree.ElementTree as ET

from core.utils import cls_, getch
from core.utils.Colors import bcolors as css

random.seed(time.time())

arts=[
    '''   ._________________.
   |.---------------.|
   ||               ||
   ||   -._ .-.     ||
   ||   -._| | |    ||
   ||   -._|"|"|    ||
   ||   -._|.-.|    ||
   ||_______________||
   /.-.-.-.-.-.-.-.-.\\
  /.-.-.-.-.-.-.-.-.-.\\
 /.-.-.-.-.-.-.-.-.-.-.\\
/______/__________\___o_\ 
\_______________________/''',
'''                         ______                     
 _________        .---"""      """---.              
:______.-':      :  .--------------.  :             
| ______  |      | :                : |             
|:______B:|      | |  Little Error: | |             
|:______B:|      | |                | |             
|:______B:|      | |  Power not     | |             
|         |      | |  found.        | |             
|:_____:  |      | |                | |             
|    ==   |      | :                : |             
|       O |      :  '--------------'  :             
|       o |      :'---...______...---'              
|       o |-._.-i___/'             \._              
|'-.____o_|   '-.   '-...______...-'  `-._          
:_________:      `.____________________   `-.___.-. 
                 .'.eeeeeeeeeeeeeeeeee.'.      :___:
               .'.eeeeeeeeeeeeeeeeeeeeee.'.         
              :____________________________:''',
              '''             ,----------------,              ,---------,
        ,-----------------------,          ,"        ,"|
      ,"                      ,"|        ,"        ,"  |
     +-----------------------+  |      ,"        ,"    |
     |  .-----------------.  |  |     +---------+      |
     |  |                 |  |  |     | -==----'|      |
     |  |  I LOVE DOS!    |  |  |     |         |      |
     |  |  Bad command or |  |  |/----|`---=    |      |
     |  |  C:\>_          |  |  |   ,/|==== ooo |      ;
     |  |                 |  |  |  // |(((( [33]|    ,"
     |  `-----------------'  |," .;'| |((((     |  ,"
     +-----------------------+  ;;  | |         |,"     
        /_)______________(_/  //'   | +---------+
   ___________________________/___  `,
  /  oooooooooooooooo  .o.  oooo /,   \,"-----------
 / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
/_==__==========__==_ooo__ooo=_/'   /___________,"
`-----------------------------' ''',
'''              ,---------------------------,
              |  /---------------------\  |
              | |                       | |
              | |     Fhvck             | |
              | |       Hackers         | |
              | |        Company        | |
              | |                       | |
              |  \_____________________/  |
              |___________________________|
            ,---\_____     []     _______/------,
          /         /______________\           /|
        /___________________________________ /  | ___
        |                                   |   |    )
        |  _ _ _                 [-------]  |   |   (
        |  o o o                 [-------]  |  /    _)_
        |__________________________________ |/     /  /
    /-------------------------------------/|      ( )/
  /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
]

emptyscreen='''
             ________________________________________________
            /                                                \ 
           |    _________________________________________     |
           |   |                                         |    |
           |   |  {main}{mainspace}|    |
           |   |  {}{s1}|    |
           |   |                                         |    |
           |   |  {}{s2}|    |
           |   |                                         |    |
           |   |  {}{s3}|    |
           |   |                                         |    |
           |   |  {}{s4}|    |
           |   |                                         |    |
           |   |                                         |    |
           |   |                                         |    |
           |   |                                         |    |
           |   |_________________________________________|    |
           |                                                  |
            \_________________________________________________/
                   \___________________________________/
                ___________________________________________
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
 _-'.-.-.-.-.-. .---.-. .-------------------------. .-.---. .---.-.-.-.`-_
:-------------------------------------------------------------------------:
`---._.-------------------------------------------------------------._.---'
''' # max width: 41

class computer():
    def __init__(self):
        # load data
        self.tree=ET.parse('core/PC/config.xml')
        self.root=self.tree.getroot()
        spaces={
            's1':' '*37,
            's2':' '*37,
            's3':' '*37,
            's4':' '*37
        }
        self.view='account'
        print(emptyscreen.format('  ','  ','  ','  ', **spaces, main='C:\> getting info...', mainspace=' '*19))
        time.sleep(1)
        self.settings()

    def settings(self):
        '''show settings'''
        cls_()
        data={}
        spaces={
            's1':' '*0,
            's2':' '*0,
            's3':' '*0,
            's4':' '*0
        }
        whr=1
        if self.view=='account':
            whr=1
        elif self.view=='graph':
            whr=0
        for child in self.root[whr]:
            data.update({child.tag:child.text})
        #del data['username']
        i=1
        for k,v in data.items():
            l=len(v)+4+len(k)
            spaces['s'+str(i)]=' '*(39-l)
            i+=1
        res=[k+' -> '+v for k,v in data.items()]
        print(emptyscreen.format(*res, **spaces, main=' '*20, mainspace=' '*19))
    
    def run(self):
        while True:
            self.settings()
            try:
                res=self.parser(input('[CMD][SET] >> '))
                if res=='end': break
            except Exception as e:
                print(e)
    
    def parser(self, x):
        cmd=x.split()[0].casefold()
        params=x.split()[1:]
        if cmd=='exit': return 'end'
        if cmd in ['custom', 'customize', 'switch', 'edit']:
            cls_()
            if not len(params):
                c=input('Editable data:\nUsername [1]\nSkin [2]\nColor [3]\n\n[*] Choose one by name or number: ').casefold()
            else:
                c=params[0]
            if c in ['1', 'username']:
                for ch in self.root[1]:
                    if ch.tag=='username':
                        ch.text=input('\nNew username: ')
                    else:
                        print(ch.tag)
            elif c in ['2', 'skin']:
                for ch in self.root[0]:
                    if ch.tag=='skin_img':
                        print('type the new icon: ')
                        r=getch().upper()
                        if r in ['M', 'R']:
                            print('Invalid icon.')
                        else:
                            ch.text=r
            elif c in ['3', 'color']:
                for ch in self.root[0]:
                    if ch.tag=='skin_clr':
                        r=input('new color: ')
                        if not r.upper() in css.__dict__.keys():
                            print('Invalid colour.')
                        else:
                            ch.text=css.__dict__[r.upper()]
            else:
                print('Invalid option.')
                return
            self.tree.write('core/PC/config.xml')
        elif cmd=='view':
            if not len(params):
                # toggle view
                if self.view=='account':
                    self.view='graph'
                elif self.view=='graph':
                    self.view='account'
            else:
                self.view=params[0]
