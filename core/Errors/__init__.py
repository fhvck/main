class ParamError(Exception):
    def __init__(self, p, additionals='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p=p
        self.a=additionals
    def __str__(self):
        return 'Unrecognized parameter:'+repr(self.p)+str(self.a)

class STDSyntaxERR(Exception):
    def __init__(self, errcmd, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmd=errcmd
    def __str__(self):
        return 'Command '+repr(self.cmd)+' Does NOT follow the standard syntax, check "'+str(self.cmd)+' -h" for more infos!'

class CommandNotFoundError(Exception):
    def __init__(self, cmd, *a, **k):
        super().__init__(*a, **k)
        self.cmd=cmd
    def __str__(self):
        return "Unrecognized command: "+repr(self.cmd)
    
class SameObjError(Exception):
    def __init__(self, a_, b, *a, **k):
        super().__init__(*a, **k)
        self.a_=a_
        self.b=b
    def __str__(self):
        return "[ERR] Object "+repr(self.a_)+" is the same of "+repr(self.b)

class HackError(Exception):
    def __init__(self, txt='', *args, **kwargs):
        self.msg=txt
    def __str__(self):
        if not len(self.msg):
            return '\033[91m[ERR]\033[0m Unable to hack.'
        else:
            return '[HACKERR]'+self.msg

class ActionRangeError(Exception):
    def __init__(self, b=None, pos=[], *a, **k):
        super().__init__(*a, **k)
        self.b=b
        self.pos=pos
    def __str__(self):
        if self.b:
            return "[ERR] Object w/ id: "+repr(self.b.id)+" is too far."
        else: 
            return "[ERR] "+repr(self.pos)+" is too far."

class DeprecationError(DeprecationWarning, Exception):
    def __str__(self):
        return 'porco d10 fermete'