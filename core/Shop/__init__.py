import json
from core.utils.Colors import bcolors as css
from core.utils import getch

class Shop():
    def __init__(self, engine):
        self.pos=[4,4]
        self.tools=json.loads(open('core/Shop/storage.json').read())
        self.commands=json.loads(open('core/Shop/commands.json').read())['commands']
        self.engine=engine
        #print(self.tools)
    
    def swindow(self):
        print('[INFO] Tools:')
        for tool in self.tools.keys(): print('-',tool)
    
    def Enter(self):
        self.engine.inshop=True
    
    def Exit(self):
        self.engine.inshop=False
    
    def shop(self, tool:str, prize:int):
        '''add the json-like object in core/cmds.json or core/Character/cmds.json'''
        #raws=json.loads(open('core/Shop/storage/raws.json').read())
        # modifica locale
        ## self.engine.commands.append(tool)
        ## self.engine.subtract_points(prize)
        # modifica i file (dumps)
        #print(tool)
        past=json.loads(open(self.tools['tools'][tool]['update_path']).read())
        past['commands'].append(tool)
        past['cheatsheet'].update({tool:self.tools['cheat_sheets'][tool]})
        f=open(self.tools['tools'][tool]['update_path'],'w')
        f.write(json.dumps(past))
        f.close()
        print('[TIP] You can use the tool after this match!')

    def parser(self, money, raw=None):
        raws=json.loads(open('core/Shop/storage.json').read())
        if not raw: raw=input(css.OKBLUE+'[SHOP]'+css.ENDC+' >> ')
        cmd=raw.split()[0].lower()
        params=raw.split()[1:]
        if not cmd in self.commands:
            print(css.OKBLUE+'[SHOP]'+css.ENDC+css.FAIL+'[ERR]'+css.ENDC+' Unrecognized command:',cmd)
            return
        else:
            if '-h' in params:
                self.docs(cmd)
                return
            
            # BUY && SHOP
            if cmd in ['buy', 'shop']:
                done=False
                print(params)
                if '-clr' in params:
                    for clr in self.tools['skins']['clrs']:
                        if clr==params[-1].casefold():
                            done=True
                            print('buy color:',css.__dict__[self.tools['skins']['clrs'][clr].upper()]+clr+css.ENDC,'? (y\\n)\n')
                            a=getch()
                            if a.casefold() in ['s','y']:
                                old=json.loads(open('core/PC/items.json').read())
                                old['mycolors'].update({clr:self.tools['skins']['clrs'][clr]})
                                f=open('core/PC/items.json','w')
                                f.write(json.dumps(old))
                                f.close()
                                return
                            else:
                                print('Annulling...')
                                return
                    if not done:
                        print('[SHOP][ERR] color:',params[-1],'doesnt exist!')
                        return
                if '-img' in params:
                    for img in self.tools['skins']['imgs']:
                        if img.casefold()==params[-1].casefold():
                            done=True
                            print('buy skin: '+repr(img)+'? (y\\n)\n')
                            a=getch()
                            if a.casefold() in ['s','y']:
                                old=json.loads(open('core/PC/items.json').read())
                                old['myimgs'].append(img)
                                f=open('core/PC/items.json','w')
                                f.write(json.dumps(old))
                                f.close()
                                return
                            else:
                                print('Annulling...')
                                return
                    if not done:
                        print('[SHOP][ERR] image:',params[-1],'doesnt exist!')
                        return
                toolname=params[0]
                if not toolname in raws['tools'].keys():
                    print('[SHOP][ERR] {tn} not found.'.format(tn=toolname)); return
                # can you buy it?
                if int(raws['tools'][toolname]['prize'])>int(money):
                    print('[SHOP][ERR] This tool costs too much!')
                    return
                else:
                    self.shop(toolname, int(raws['tools'][toolname]['prize']))
            
            # EXIT
            elif cmd in ['bye', 'exit']:
                self.engine.inshop=False
            
            # SHOP WINDOW
            elif cmd in ['swindow', 'show']:
                if '-q' in params:
                    # solo gli acquistabili
                    for tool in self.tools['tools']: # globals, locals
                        #print(css.OKCYAN+'[INFO]'+css.ENDC+' type:',tmode)
                        if not len(self.tools['tools']):
                            print(' - no tools here.'); break
                        for tool in self.tools['tools']:
                            if int(self.tools['tools'][tool]['prize'])>int(money):
                                pass
                            else:
                                print(css.OKBLUE+'-'+css.ENDC,tool)
                    print(css.HEADER+'[*]'+css.ENDC+'skins:')
                    print('----\nimages:')
                    i=0
                    for img in self.tools['skins']['imgs']:
                        if i<=4:
                            print(img, end=' ')
                        else:
                            print('\n',img,end=' ')
                        i+=1
                    print('----\ncolors:')
                    i=0
                    for clr in self.tools['skins']['clrs']:
                        if i<=4:
                            print(clr, end=' ')
                        else:
                            print('\n',clr,end=' ')
                        i+=1
                else:
                    print(css.HEADER+'[*]'+css.ENDC+' Tools:')
                    if not len(self.tools['tools']):
                        print(' - no tools here.')
                    for tool in self.tools['tools']:
                        print(css.OKBLUE+'-'+css.ENDC,tool)
                    print(css.HEADER+'[*]'+css.ENDC+' Skins:')
                    print('----\nimages:')
                    i=0
                    for img in self.tools['skins']['imgs']:
                        if i<=4:
                            print(img, end=' ')
                        else:
                            print('\n',img,end=' '); i=-1
                        i+=1
                    print('\n----\ncolors:')
                    i=0
                    for clr in self.tools['skins']['clrs']:
                        print(css.__dict__[self.tools['skins']['clrs'][clr].upper()]+clr+css.ENDC)
            
            # HELP
            elif cmd=='help':
                if not len(params):
                    print(css.HEADER+'[H]'+css.ENDC+' List of commands:')
                    [print('-',c) for c in self.commands]; print(css.HEADER+'[H]'+css.ENDC+' type "cmd -h" for additiona help about "cmd"')
                else:
                    try:
                        self.docs(params[0])
                    except:
                        print(css.FAIL+'[ERR]'+css.ENDC+' Unknown command', cmd)
            
            # INFO
            elif cmd in ['desc', 'info']:
                if cmd=='desc':
                    if not len(params): print(css.FAIL+'[ERR]'+css.ENDC+' No tool specified.'); return
                    if '-tool' in params:
                        tool=params[params.index('-tool')+1]
                    else:
                        tool=params[0]
                    self.Tdocs(tool)
                else:
                    if not len(params):
                        for tool in self.tools:
                            self.Tdocs(tool)
                    else:
                        if '-tool' in params:
                            tool=params[params.index('-tool')+1]
                        else:
                            tool=params[0]
                        self.Tdocs(tool)
            
            # REGIVE
            elif cmd=='regive':
                if not '-tool' in params:
                    toolname=params[0]
                else:
                    toolname=params[params.index('-tool')+1]
                #raws_=json.loads(open('core/Shop/storage/raws.json').read())
                #specs=json.loads(open('core/Shop/storage/tools.json').read())
                #indx=str(raws[toolname])
                upath=raws['tools'][toolname]['update_path']
                old=json.loads(open(upath).read())
                new=old['commands'].remove(toolname)
                del new['cheat_sheets'][toolname]
                f=open(upath, 'w')
                f.write(json.dumps(new))
                f.close()
                del f
                self.engine.subtract_points(-abs(round(int(self.tools['tools'][toolname]['prize'])/2)))
    
    def Tdocs(self, man):
        data=json.loads(open('core/Shop/storage.json').read())
        if not man in data['cheat_sheets'].keys(): return
        for k in data['cheat_sheets'][man]:
            print(k,data['cheat_sheets'][man][k])
        return
    
    def docs(self, man):
        data=json.loads(open('core/Shop/cmds.json').read())
        for key in data['cheatsheet'][man]:
            print(key,css.WARNING+'->'+css.ENDC,data['cheatsheet'][man][key])