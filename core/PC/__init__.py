from core.utils import ParserGet, ParserSetup

class computer():
    def __init__(self):
        # load data
        pass

    def settings(self):
        '''show settings'''
        return

    @ParserGet
    @ParserSetup
    def parser(self, x, p=[]):
        if x=='help':
            print('ti aiuto io sk')
        else:
            print('boh')

