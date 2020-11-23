import base64
import json
import os
import random
import sys
import time
import xml.etree.ElementTree as ET

import core.Errors as errs
import core.PC
from core.Characters import Player, Robot
from core.PC import computer
from core.Recognition.botdata.graph import arts as botskins
from core.Recognition.botdata.graph import specs as botgraphs
from core.Shop import Shop
from core.utils import *
from core.utils.Colors import bcolors as css
import core.Recognition as reco
import core.Smtp as smtp

random.seed(time.time())

# load screens
# no non me va piu bruh

points={
    "win":10,
    "kill":1
}

Box=smtp.MailBox()

class Engine():
    def __init__(self, col=4, rows=5, enems=1, img='U', clr=css.OKBLUE):
        tree=ET.parse('core/PC/config.xml')
        root=tree.getroot()
        for child in root[1]:
            if child.tag=='points':
                self.gamepoints=int(child.text); break
        # map setup
        self.columns=col
        self.rows=rows
        self.map=[['_' for _ in range(rows+1)] for _ in range(col+1)]
        self.u=clr+img+css.ENDC
        # match maker setup
        self.robots=[Robot(self) for _ in range(enems)]
        self.player=Player(col, rows, self)
        self.robots.append(self.player)
        # external objs setup
        self.shop=Shop(self)
        self.Team=reco.RecoSquad(self)
        # graphic settings
        self.showids=False
        self.showpos=False
        self.overrideshow=False
        self.inbshell=False
        self.inshop=False
        self.inreco=False

    def run(self):
        while True:
            if not len(self.robots) or (len(self.robots)==1 and self.robots[0]==self.player):
                self.win(); break
            self.update_map()
            # BSHELL LOOP
            while self.inbshell:
                try:
                    self.player.selected.BShell(input(css.OKCYAN+'[CMD]'+css.ENDC+css.OKGREEN+'[BSH]'+css.ENDC+' >> '))
                except IndexError:
                    print(css.FAIL+'[ERR]'+css.ENDC+' Missing a parameter.')
                except Exception as e:
                    print(css.FAIL+'[ERR]'+css.ENDC,str(e))
            # SHOP LOOP
            while self.inshop:
                try:
                    self.shop.parser(self.gamepoints)
                except IndexError:
                    print(css.FAIL+'[ERR]'+css.ENDC+' Missing a parameter')
            # RECO LOOP
            while self.inreco:
                self.Team.parser(input(css.HEADER+'[RECO]'+css.ENDC+'>> '), self.player)
            try:
                if self.player.selected:
                    # BOT LOOP
                    self.player.selected.parser(input(css.OKGREEN+'[BOT]'+css.ENDC+css.OKCYAN+'[SCORE:{}]'.format(self.gamepoints)+css.ENDC+' -state:{}- >> '.format(self.player.selected.state)))
                else:
                    # MAP LOOP
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
        
        # SHOP
        elif cmd=='shop':
            self.inshop=True
            if '-s' in params or '--show' in params:
                pass
        
        # RECO
        elif cmd in ['reco', 'recognitors']:
            if not len(params):
                self.Team.parser('',self.player)
            else:
                self.Team.parser(' '.join(params), self.player)

        # NOT FOUND        
        else:
            raise errs.CommandNotFoundError(cmd)
    
    def win(self):
        self.gamepoints+=10
        cls_()
        titles=[
            '__   _____  _   _  __        _____ _   _ \n\\ \\ / / _ \\| | | | \\ \\      / /_ _| \\ | |\n \\ V / | | | | | |  \\ \\ /\\ / / | ||  \\| |\n  | || |_| | |_| |   \\ V  V /  | || |\\  |\n  |_| \\___/ \\___/     \\_/\\_/  |___|_| \\_|\n                                         \n',
            '                                                \n# #      #      # #         # #     ###     ### \n# #     # #     # #         # #      #      # # \n #      # #     # #         ###      #      # # \n #      # #     # #         ###      #      # # \n #       #      ###         # #     ###     # # \n'
            ]
        tree=ET.parse('core/PC/config.xml')
        root=tree.getroot()
        root[1][1]=int(root[1][1])+self.gamepoints
        tree.write('core/PC/config.xml')
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
                                self.map[y][x]=css.OKBLUE+self.u+css.ENDC; done=True
                        elif self.showids:
                            self.map[y][x]=bot.color+str(bot.id)+css.ENDC; done=True
                        elif self.showpos:
                            self.map[y][x]=bot.color+','.join([str(p) for p in bot.pos])+css.ENDC; done=True
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

def loadconfig():
    tree=ET.parse('core/PC/config.xml')
    root=tree.getroot()
    # game=0, account=1
    res={}
    for child in root[0]:
        if 'kwarg' in child.attrib.keys():
            if child.attrib['kwarg']=='clr':
                res.update({child.attrib['kwarg']:css.__dict__[child.text.upper()]})
                continue
            elif child.attrib['kwarg']=='img':
                res.update({child.attrib['kwarg']:child.text})
                continue
            res.update({child.attrib['kwarg']:int(child.text)})
    return res


def main(*oth):
    if not oth:
        print(" _____ _              _    \n|  ___| |____   _____| | __\n| |_  | '_ \\ \\ / / __| |/ /\n|  _| | | | \\ V / (__|   < \n|_|   |_| |_|\\_/ \\___|_|\\_\\\n                  version: 0.1alpha        \n")
        print('\n\t'+css.OKGREEN+'NEW GAME [1]'+css.ENDC+'\n\t'+css.WARNING+'CUSTOMIZE [2]'+css.ENDC+'\n\t'+css.FAIL+'EXIT [0]'+css.ENDC)
        ch=getch()
        if ch=='1':
            cls_()
            game=Engine(**loadconfig())
            game.run()
        elif ch=='2':
            pass
        elif ch in ['3','0']:
            print('[*] Exiting...')
            exit()
    else:
        print(*oth)

    x=input('\n\n$[MAIN] >> ')
    if not x: main('no command given.')
    cmd=x.split()[0].casefold()
    params=x.split()[1:]
    cls_()
    if cmd in ['.start','start']:
        game=Engine()
        game.run()

    elif cmd in ['./mypc', 'pc', '.pc', 'mypc', '.mypc']:
        computer().run()
        cls_(); main()

    elif cmd in ['exit', 'bye']:
        print('[*] Exiting...')
        main()
    
    elif cmd=='help':
        main('startup info utility [v-0.1alpha]\ncommands:\n\nstart  -> launch the game\nmypc   -> read or change settings\nbye    -> exit the game\n\n')

    else:
        main('[ERR] Unrecognized command:',cmd)

def intro():
    print('Hey, looks like u r new here! choose a language:\n[1] IT - italian\n[2] EN - english\n')
    c=getch()
    if c=='1':
        lang='it'
    elif c=='2':
        print('metto comunque ita perchè non ho sbatti di tradurre tutto :o')
        lang='it'
    else:
        print('invalid choose.')
        intro()
    if lang=='it':
        cls_()
        print("Benvenuto, io sono l'ex comandante di questa base. da adesso comanderai tu questo posto, ma prima dimmi, come ti chiami?\n")
        usrname=input()
        print('\nPerfetto, dammi un attimo di tempo per sistemare il tuo chip')
        chargebar('updating...')
        chargebar('checking...')
        chargebar('installing...')
        print('Fantastico! adesso il tuo chip personale è settato per te. grazie a questo chip potrai comprare dal negozio ed essere riconosciuto online.')
        print('non puoi leggere il chip direttamente ma il tuo computer può farlo, ti porto subito a vedere come.')
        print('premi un tasto qualsiasi per continuare.'); getch()
        chargebar('Entering the pc...')
        cls_()
        spaces={
            's1':' '*37,
            's2':' '*37,
            's3':' '*37,
            's4':' '*37
        }
        print(core.PC.emptyscreen.format('  ','  ','  ','  ', **spaces, main='C:\> your pc!', mainspace=' '*26))
        print('\nQuesto è il tuo computer, da qui puoi vedere tutte le cose che sono scritte nel tuo chip e anche modificarne alcune.')
        print('il tuo computer puo anche modificare le impostazioni della partita come ad esempio le dimensioni della mappa')
        print('ovviamente il computer accetta dei comandi per poter compiere lazione richiesta ma quali? andiamo a vederlo ora.')
        print('premi un tasto qualsiasi per continuare.'); getch()
        chargebar('getting back...')
        cls_()
        print('qualsiasi comando qui segue una sintassi di base chiamata STDSYX o comunemente SYX, questo nome significa STANDARD SYNTAX.')
        print('avendo un certo comando "cmd" per lanciarlo (eseguirlo) scriviamo\n'+css.BOLD+'cmd'+css.ENDC+'\nquesto eseguira cmd.')
        print('prendiamo come esempio il comando "show" che mostra qualcosa sulla mappa e ammettiamo di voler mostrare gli id, come facciamo a dire')
        print('a show di mostrare proprio gli id? show ha una scrittura semplificata per cui basterà scrivere:\n'+css.BOLD+'show id'+css.ENDC)
        print('ma se volessimo seguire la syx scriveremmo:\n'+css.BOLD+'show -e id'+css.ENDC+'\n'+"cos'è cambiato? la syx prevede questo tipo di scrittura:")
        print(css.BOLD+'cmd -var val'+css.ENDC+'\nper eseguire cmd con var=val, prima infatti abbiamo eseguito show con e=id (e sta per element)')
        print('premi un tasto per continuare..')
        getch()
        chargebar('Exiting base...')
        chargebar('Entering fight camp...')
        cls_()
        print('purtroppo la pace è finita e siamo costretti a respingere i Robot che tentano di distruggere la base, per fermarli cè un solo modo, distruggerli')
        print('tutti, uno per uno. la tua base ha una squadra di ricognizione che da tempo studia questi Robot assalitori e ha scoperto delle cose di vitale importanza.')
        print('ti mostro subito lo schema di un robot:')
        chargebar('gaining informations...')
        bot_introspection=ET.parse('core/Recognition/botdata/bot.xml').getroot()
        def goto1():
            cls_()
            print(botskins[0])
            print("\nQuesta è la struttura di un Robot standard, premi il numero corrispondente per effettuare l'introspezione di quel punto, 0 per continuare")
            r=getch()
            if r=='0':
                return
            elif r=='1':
                # head
                cls_()
                print(botgraphs['head'])
                print('\nDa qui il robot può osservare i tuoi spostamenti sulla mappa, al suo interno ci sono i convertitori che andranno a contattare la scheda')
                print("all'interno del body. quando hackeri un robot vai a disabilitare queste connessioni così da spegnere i suoi sistemi di sicurezza.")
                print('press any key.'); getch()
                goto1()
            elif r=='2':
                # body
                cls_()
                print(botgraphs['body'])
                print('\nQuesta è la scheda che viene contattata dalla head quando un qualsiasi comando sta per essere eseguito. se questo comando viene giudicato')
                print('pericoloso viene inviato un segnale alla head ordinando di bloccare il comando, interrompendo quindi lesecuzione di comandi come shutdown. ')
                print('qui sono presenti le porte da cui il Robot contatta gli altri bot e il suo stesso sistema di sicurezza, e questo il punto che devi colpire per primo.')
                print('press any key.'); getch()
                goto1()
            elif r=='3':
                # legs
                cls_()
                print(botgraphs['legs'])
                print('\nQuesto sistema è usato dal Robot per spostarsi sulla mappa, il range di spostamento del robot dipende dalla lunghezza delle gambe,')
                print('più le gambe sono corte e minore sarà il range di azione, puoi controllare questo sistema solo dalla bshell.'); getch()
                goto1()
            elif r=='4':
                # cannons
                cls_()
                print(botgraphs['cannons'])
                print('\niI nostri ricognitori sono riusciti a disabilitare questo sistema di attacco su tutti i Robot ma si vocifera la costruzione di alcuni robot')
                print('capaci di ignorare il nostro blocco e attaccare ugualmente, ma attualmente è solo una voce.')
                print('press any key.'); getch()
                goto1()
            else:
                print('Invalid value.')
                print('press any key.'); getch()
                goto1()
        goto1()
        cls_()
        print('Bene, ora che hai un idea sul funzionamento dei Robot possiamo vedere COME attaccarne uno.')
        print('press any key.'); getch()
        cls_()
        def goto2(text=None):
            cls_()
            fmap=lambda x: print() if x==5 else print('_', end=' ')
            [[fmap(i) for i in range(0,6)] for _ in range(0,5)]
            print('\nQuesta è la mappa, qui puoi vedere te, i robot e i punti in cui entrambi potete spostarvi. ogni posizione è chiamata "tile"')
            print('un tile vuoto viene indicato con un underscore ("_") mentre un tile occupato prende di norma limmagine del carattere che la occupa.')
            print('un robot ha la lettera R come immagine, rossa se il robot è bloccato, verde se è gia sbloccato o stato hackerato. tu sei rappresentato con una U blu.')
            print('in questa schermata come in qualsiasi altra abbiamo SICURAMENTE disponibile il comando help, quindi proviamo a scrivere "help":')
            if text: print(text)
            x=input(css.OKGREEN+'[MAP]'+css.ENDC+css.OKCYAN+'[SCORE:{}]'.format('0')+css.ENDC+' >> ')
            if not x.casefold()=='help':
                goto2(str(errs.CommandNotFoundError(x)))
            print(css.HEADER+'[*]'+css.ENDC+' List of commands:')
            [print(command) for command in json.loads(open('core/commands.json').read())['commands']]
            print("\nCome vedi help restituisce una lista dei comandi ma senza spiegarne la sintassi ne l'utilizzo, come facciamo?")
            print("grazie alla syx sappiamo che ogni comando ha (fortunatamente) il parametro -h che se specificato mostra la documentazione del comando.")
            print('senza leggere tutte le documentazioni possiamo farci un idea di come funzioni un comando solo dal nome, ad esempio show.')
            print('show serve a modificare la vista della mappa, la sua sintassi è:\n'+css.OKGREEN+'>'+css.ENDC+css.BOLD+' show id||pos -a'+css.ENDC)
            print('id||pos significa id OR pos, quindi una delle due possibilità (in realtà possiamo scrivere show null per tornare ala vista di default)')
            print('se -a (a sta per "all") viene specificato allora mostra anche i dati del player (i tuoi) oltre che dei nemici.')
            print('un altro comando importantissimo è select che serve, come suggerisce il nome, a selezionare un robot dalla mappa. questo comando ci mette')
            print('in comunicazione con la head, la parte che credo tu abbia visto durante l introspezione di un robot. vediamo la sintassi di select.')
            print(css.OKGREEN+'> '+css.ENDC+css.BOLD+'select -id||-pos value'+css.ENDC+'\n-id or -pos serve a dichiarare quale tipo di valore stiamo per inserire e value')
            print('è proprio questo valore. se vogliamo selezionare il bot con id=52 scriveremo "select -id 52", se invece vogliamo usare la posizione di un robot con x=3 e y=4 scriviamo')
            print('"select -pos 3,4". la cosa importante da notare è che x,y vada scritto senza spazi altrimenti non verrà riconosciuto.')
            print('la domanda che viene spontanea è dove prendiamo i valori di cui necessitiamo? sarà la mappa a fornirceli, con show id vediamo tutti gli id, ne scegliamo uno e poi')
            print('con "select -id IDSCELTO" usiamo IDSCELTO per far capire alla mappa quale bot intendiamo.','\npress any key'); getch()
            cls_()
            print('adesso con select abbiamo selezionato un Robot e siamo nella sua head. cosa fare? per vincere un combattimento dobbiamo distruggere tutti i robot quindi')
            print('spegniamoli tutti. attualmente non hai tanti strumenti a disposizione, puoi comprarli dallo shop ma fino a quel momento dovrai farti bastare questi che hai già.')
            print('tornando a noi, lo schema da seguire per distruggere un Robot è:\n1. bypassare una porta\n2. usare la porta per hackerarlo\n3. spegnerlo')
            print("andiamo in ordine, per bypassare una porta dobbiamo:\n1. ottenere il suo hash\n2. decodificarlo\n3. usare l'hash decodificato per bypassarla")
            print('quindi prima di tutto otteniamo il suo hash, come? il comando hash serve proprio a questo. scrivi "hash" per vedere tutte le porte con il relativo hash:')
            def goto3():
                x=input(css.OKGREEN+'[MAP]'+css.ENDC+css.OKCYAN+'[SCORE:{}]'.format('0')+css.ENDC+' >> ')
                if not x.casefold()=='hash':
                    print(str(errs.CommandNotFoundError(x)))
                    goto3()
                hashes={'80':'aGFzaDE=','443':'Mmhhc2g='}
                print(css.HEADER+'hashes:'+css.ENDC)
                [print(css.OKCYAN+'[HASH]'+css.ENDC,key,hashes[key]) for key in hashes.keys()] # FIXME scrive tre volte "hashes:\nport hash\nport hash" # si è fixato da solo wtf
            goto3()
            print('\nQui trovi gli hash scritti "porta hash", copiane uno ("=" incluso) e passiamo al prossimo step.'); getch()
            cls_()
            def goto4():
                choosedport='80'
                print('adesso che abbiamo un hash dobbiamo decodificarlo. per farlo usiamo decoder. la sua sintassi è:\n'+css.OKGREEN+'> '+css.ENDC+'decoder -text testo')
                print("questo decodificherà 'testo' quindi andiamo a sostituire testo con il nostro hash. ora"+' "decoder -text incolla_qui"')
                print("P.S. se ti fossi dimenticato di copiare il valore o lo avessi perso puoi usare questo:\naGFzaDE=\nche è l'hash della porta 80.")
                x=input(css.OKGREEN+'[MAP]'+css.ENDC+css.OKCYAN+'[SCORE:{}]'.format('0')+css.ENDC+' >> ')
                if x.casefold().split()[0]=='decoder' and x.casefold().split()[1]=='-text' and x.split()[2] in ['aGFzaDE=','Mmhhc2g=']:
                    if x.split()[2]=='aGFzaDE=':
                        choosedport='80'
                    else:
                        choosedport='443'
                    print(css.HEADER+'[*]'+css.ENDC+' Decoded text: '+css.OKBLUE, base64.b64decode(x.split()[2]).decode(),css.ENDC)
                    return choosedport
                else:
                    print('Invalid syntax.'); return goto4()
            choosedport=goto4()
            print('\nDecoder ha restituito la versione decifrata del tuo testo. adesso usa questa versione decifrata per bypassare una porta.')
            print('usiamo lo stesso comando di prima, hash. la sua sintassi è\n'+css.OKGREEN+'> '+css.ENDC+'hash -port p -res decodedhash\nnoi prima abbiamo scritto hash e basta,')
            print('questo mostra tutte le porte con relativi hash, se avessimo specificato una porta avrebbe mostrato solo quella porta specificata.')
            print('-res è opzionale come port, se specificato invece di mostrare gli hash ne usa uno per sbloccare una porta specificata. esempio:')
            print("hash -res abcde -port 80\nusa abcde per sbloccare la porta 80, al posto di abcde dobbiamo inserire la versione decifrata dell'hash della porta 80")
            print("se hai decifrato l'hash della porta 80 scrivi:\nhash -res incolla_qui -port 80\nse quello della 443:\nhash -res incolla_qui -port 443")
            print('non dimenticare di sostituire incolla_qui con il risultato di decoder! proviamo:')
            def goto5():
                x=input(css.OKGREEN+'[MAP]'+css.ENDC+css.OKCYAN+'[SCORE:{}]'.format('0')+css.ENDC+' >> ')
                ths=x.casefold().split()
                if ths[0]=='hash' and ths[1]=='-res' and ths[2] in ['hash1', '2hash'] and ths[3]=='-port' and ths[4] in ['80', '443']:
                    if (ths[2]=='hash1' and ths[4]=='80') or (ths[2]=='2hash' and ths[2]=='443'):
                        print(css.HEADER+'[*]'+css.ENDC+' Port {p} Successfully bypassed.'.format(p=ths[4]))
                    else:
                        print('cannot bypass, hash incorrect for this port.'); goto5()
                else:
                    print('Invalid syntax.'); goto5()
            goto5(); getch()
            cls_()
            print('Perfetto! hai appena bypassato una porta per la prima volta, adesso hai fatto il 90%% del lavoro. il nostro obiettivo è quello di spegnere un robot quindi procediamo.')
            print('il prossimo comando da usare è hack. questo usa una porta sbloccata per disabilitare i sistemi di sicurezza del robot. la sua sintassi è:\nhack -port p')
            print('ammettendo che p sia il numero di una porta sbloccata. adesso usiamolo per disabilitare i sistemi di questo bot, scrivi:\nhack -port portascelta')
            print('sostituendo portascelta con la porta dalla quale avevi copiato gli hash, nel nostro caso {}'.format(choosedport))
            print('proviamo quindi ad hackerare il robot usando la porta sbloccata:')
            def goto6():
                x=input(css.OKGREEN+'[MAP]'+css.ENDC+css.OKCYAN+'[SCORE:{}]'.format('0')+css.ENDC+' >> ')
                try:
                    if x.split()[0].casefold()=='hack' and x.split()[1]=='-port' and x.split()[2] in ['80','443']:
                        if not str(x.split()[2])==str(choosedport):
                            print(errs.HackError()); goto6()
                        else:
                            print(css.OKCYAN+'[..]'+css.ENDC+' Hacking on port:',choosedport)
                            time.sleep(0.5)
                            print(css.OKCYAN+'[*]'+css.ENDC+css.OKGREEN+' Successfully hacked.'+css.ENDC)
                    else:
                        print('command or syntax r invalid, or maybe the port is incorrect!')
                        goto6()
                except:
                    print('an error has occured.')
                    goto6()
            goto6()
            print('\nhai correttamente hackerato il robot! adesso non ha più i sistemi di sicurezza abilitati e nulla ci impedirà di distruggerlo.')
            print('il prossimo comando è destroy che non ha parametri ne nulla, basta scrivere destroy (o shutdown, stesso comando ma diverso nome)')
            print('proviamo:')
            def goto7():
                x=input(css.OKGREEN+'[MAP]'+css.ENDC+css.OKCYAN+'[SCORE:{}]'.format('0')+css.ENDC+' >> ')
                if x.casefold() in ['destroy', 'shutdown']:
                    print(css.FAIL+'[..]'+css.ENDC+' Self-Destruction Enabled..')
                    time.sleep(0.4)
                    print(css.HEADER+'[*]'+css.ENDC+' Bot killed.')
                else:
                    print('puoi scrivere solo shutdown o destroy.')
                    goto7()
            goto7()
            print('\nWOOOOHOOOO, hai ucciso il tuo primo robot, come crescono in fretta *lacrimuccia*.')
            print('da adesso le cose si faranno più difficili, a differenza di adesso avrai carta bianca e potrai eseguire ogni comando quando vorrai')
            print('sempre ammesso che funzionerà :)')
            print('potrai ripetere il tutorial quando vorrai, basta scrivere "tutorial -repeat" nella schermata home.')

        goto2()


    return {
        "username":usrname,
        "points":"0",
        "wins":"0",
        "kills":"0"
    }


# check if is the first launch
if not 'config.xml' in os.listdir('core/PC/'):
    root=ET.Element('SETTINGS')
    # game settings
    game=ET.SubElement(root,'game')
    # enemies number
    enems=ET.SubElement(game, 'lvl1_enemies')
    enems.attrib['kwarg']='enems'; enems.text='3'
    # skin img
    skimg=ET.SubElement(game, 'skin_img')
    skimg.attrib['kwarg']='img'; skimg.text='U'
    # skin clr
    skclr=ET.SubElement(game, 'skin_clr')
    skclr.attrib['kwarg']='clr'; skclr.text='okblue'
    # columns
    cols=ET.SubElement(game, 'map_columns')
    cols.attrib['kwarg']='col'; cols.text='4'
    # rows
    rws=ET.SubElement(game, 'map_rows')
    rws.attrib['kwarg']='rows'; rws.text='5'
    # GET INFO FROM THE INTRO
    data=intro() # FIXME wtf dopo un introduzione non scrive il file xml e ricomincia. 
    # boh eseguita nella shell di debug funziona, non so proprio cosa dire..
    account=ET.SubElement(root, 'account')
    for k, v in data.items():
        nsv=ET.SubElement(account, k)
        nsv.text=v
    # write
    tree = ET.ElementTree(root)
    tree.write('core/PC/config.xml')

#main()
Box.render('*')
Box.new_mail('sto cazzo', 'greatings', 'how r you bro?')
Box.render('*')