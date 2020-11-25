import base64
import random
import time

import arcade

random.seed(time.time())

class Kernel():
    def __init__(self):
        self.islocked=True
        self.is_active=True
        self.ports={'80':1, '443':1}
        self.hashes={}
        [self.hashes.update({port:base64.b64encode(''.join([chr(random.randint(97,122)) for _ in range(5)]).encode()).decode()}) for port in self.ports.keys()]

class Player(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(30, 30, arcade.color.BLUE)
    
    def on_tap(self):
        return 'cant select urself!'

class Robot(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(30, 30, arcade.color.RED)
        self.id=random.randint(10, 1000)
        self.kernel=Kernel()
    
    def on_tap(self):
        return 'helo im'+str(self.id)


class Tile(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(30, 30, arcade.color.WHITE)
        self.isplayer=False
        self.isrobot=False
    
    def to_robot(self):
        self.id=random.randint(10, 1000)
        self.color=arcade.color.RED
        self.kernel=Kernel()
        self.isrobot=True
        self.isplayer=False
    
    def to_player(self):
        self.color=arcade.color.GREEN
        self.isplayer=True
        self.isrobot=False
    
    def on_tap(self):
        if self.isrobot:
            print('helo im '+str(self.id))
        elif self.isplayer:
            print('cant select yourself')
    
    def parser(self, cmd, params):
        # TODO add the bot parser
        print('bot parser w/:',cmd,params)
