import sys, os
from functools import wraps
import time, sys

def cls_():
    if sys.platform.lower()=="linux":
        os.system("clear")
    else:
        os.system('cls')

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch().decode()


getch = _Getch()

def list_splice(target, start, delete_count=None, *items):
    if delete_count == None:
        delete_count = len(target) - start

    # store removed range in a separate list and replace with *items
    total = start + delete_count
    removed = target[start:total]
    target[start:total] = items

    return removed

def ParserGet(func:'if chain'):
    def wrapper(*args, **kwargs):
        x=args[1] # [0] sarebbe self
        cmd=x.split()[0].casefold()
        params=x.split()[1:]
        func(cmd, params)
    return wrapper

def ParserSetup(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        cmd=args[0]
        params=args[1:]
        return func(self=self, x=cmd, p=params)
    return wrapper

def chargebar(inner_text):
    toolbar_width=len(inner_text)
    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    for i in range(toolbar_width):
        time.sleep(0.1) # do real work here
        # update the bar
        sys.stdout.write(inner_text[i])
        sys.stdout.flush()

    sys.stdout.write("] \033[92mDONE!\033[0m\n") # this ends the progress bar
