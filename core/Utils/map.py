from core.Utils.colors import bcolors as css
import core.Errors as errs
import json

def map_parser(cmd, params):
    # TODO add funcs to this parser
    if '-h' in params:
        raise NotImplementedError

    # HELP
    if cmd=='help':
        if not len(params):
            print(css.HEADER+'[*]'+css.ENDC+' List of commands:')
            [print(command) for command in json.loads(open('core/commands.json').read())['commands']]
        else:
            raise NotImplementedError
    
    # SHOW
    elif cmd=='show':
        raise errs.DeprecationError()
        overrideshow=False
        if '-a' in params:
            overrideshow=True
        if 'id' in params or '-id' in params:
            showids=True
            showpos=False
        elif 'pos' in params or '-pos' in params:
            showids=False
            showpos=True
        elif 'null' in params or '-null' in params:
            showids=False
            showpos=False
        else:
            raise errs.ParamError(params)
        return ['showupdate', showids, showpos, overrideshow]
    
    # SELECT
    elif cmd=='select':
        pass # now mouse click

    # MOVE
    elif cmd=='move':
        pass # now mouse drag
    
    # EXIT && BYE
    elif cmd in ['bye', 'exit']:
        pass # now ESC key
    
    # SHOP
    elif cmd=='shop':
        raise NotImplementedError()
    
    # RECO
    elif cmd in ['reco', 'recognitors']:
        raise NotImplementedError

    return [None]