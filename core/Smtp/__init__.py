import ast
import json
import xml.etree.ElementTree as ET

from core.utils.Colors import bcolors as css

pallino=css.OKBLUE+'*'+css.ENDC
data={}

class MailBox():
    def __init__(self):
        global data
        self.res=json.loads(open('core/SMTP/archive.json').read())
        self.boxTree=ET.parse('core/SMTP/archive.xml')
        self.box=self.boxTree.getroot()
        self.parent_map = {c:p for p in self.boxTree.iter() for c in p}
        # dividi lette da non lette
        self.emails={}
        #self.emails.update({str(self.res[mail.text]['Body']):mail} for mail in self.box[0])
        for at in self.box:
            for email in at:
                self.emails.update({str(self.res[email.text]):email})
    
    def render(self, mode='d'):
        f=lambda x: 1 if x=='True' else 0
        f_=lambda x: '<you>' if x=='sent' else '<!U>'
        possibilities=['*', 'r', 'u', 's', 'd'] # all, read, unread, sent, std
        #print(self.parent_map)
        if mode=='*':
            for key, mail in self.emails.items():
                r=ast.literal_eval(key)
                if bool(f(mail.attrib['seen'])):
                    print(f_(self.parent_map[mail].tag), r['Title'], '['+str(list(self.emails.keys()).index(key))+']',pallino)
                else:
                    print(f_(self.parent_map[mail].tag), r['Title'], '['+str(list(self.emails.keys()).index(key))+']')
        elif mode=='d':
            for key, mail in self.emails.items():
                r=ast.literal_eval(key)
                if f_(self.parent_map[mail].tag)=='<you>': continue
                if bool(f(mail.attrib['seen'])):
                    print(f_(self.parent_map[mail].tag), r['Title'], '['+str(list(self.emails.keys()).index(key))+']',pallino)
                else:
                    print(f_(self.parent_map[mail].tag), r['Title'], '['+str(list(self.emails.keys()).index(key))+']')
    
    def new_mail(self, to:str, title:str=None, body:str=None):
        if not title and not body:
            print('entering the editor')
        elif not title and body:
            print('choose a title')
        elif title and not body:
            print('write the text')
        # now u have all the infos, write a mail
        template={
            "Title":title,
            "Body":body
        }; i=1
        for key in self.res: i+=1
        self.res.update({'path'+str(i):template})
        if not title or not body:
            print('error, bool() title or body is False.')
            return
        f=open('core/SMTP/archive.json','w+')
        f.write(json.dumps(self.res))
        f.close() # updated json, now update xml
        newmail=ET.SubElement(self.box[1], 'email', attrib={'seen':'False'})
        newmail.text='path'+str(i)
        self.boxTree.write('core/SMTP/archive.xml')
        self.__init__()