import json
import random
import time

import arcade
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.ui_style import UIStyle

from core.Characters import *
from core.Errors import *
from core.Utils import map_parser

random.seed(time.time())

ROW_COUNT = 15
COLUMN_COUNT = 15

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Array Backed Grid Buffered Example"
SCREEN_WIDTH+=250

# Game settings r actually consts :(
enemiesNum=5

# DEFINE SOME COLORS
lockedRobotColor=arcade.color.RED
unlockedRobotColor=arcade.color.GREEN
PlayerColor=arcade.color.CYAN

selectedbot=None

# load commands
map_commands=json.loads(open('core/commands.json').read())
bot_commands=json.loads(open('core/Characters/commands.json').read())

class MyGhostFlatButton(arcade.gui.UIGhostFlatButton):
    """
    For this subclass, we create a custom init, that takes in another
    parameter, the UI text box. We use that parameter and print the contents
    of the text entry box when the ghost button is clicked.
    """

    def __init__(self, center_x, center_y, input_box):
        super().__init__(
            'Send',
            center_x=center_x,
            center_y=center_y,
            width=150,
            height=51
        )
        self.input_box = input_box

    def on_click(self):
        """ Called when user lets off button """
        print(f"Click ghost flat button. {self.input_box.text}")
        if not self.input_box.text: return
        cmd=self.input_box.text.split()[0].casefold()
        params=self.input_box.text.split()[1:]
        # TODO aggiungi dei catch generici per gestire gli errori che raisa.
        if selectedbot:
            if not cmd in bot_commands['commands']:
                print(CommandNotFoundError(cmd))
                return
            selectedbot.parser(cmd, params)
        else:
            if not cmd in map_commands['commands']:
                print(CommandNotFoundError(cmd))
                return
            map_parser(cmd, params)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list = arcade.SpriteList()

        # This will be a two-dimensional grid of sprites to mirror the two
        # dimensional grid of numbers. This points to the SAME sprites that are
        # in grid_sprite_list, just in a 2d manner.
        self.grid_sprites = []
        # Create a list of solid-color sprites to represent each grid location
        for row in range(COLUMN_COUNT):
            self.grid_sprites.append([])
            for column in range(ROW_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = Tile()
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)
        # spawn bots
        for _ in range(enemiesNum+1):
            self.grid_sprites[random.randint(0,ROW_COUNT-1)][random.randint(0,COLUMN_COUNT-1)].to_robot()
        self.grid_sprites[random.randint(0,ROW_COUNT-1)][random.randint(0,COLUMN_COUNT-1)].to_player()
    
    def setup(self):
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 4
        right_column_x = 3 * self.window.width // 4

        ui_input_box = arcade.gui.UIInputBox(
            center_x=right_column_x+65,
            center_y=y_slot * 3,
            width=240
        )
        ui_input_box.text = 'type here.'
        ui_input_box.cursor_index = len(ui_input_box.text)
        self.ui_manager.add_ui_element(ui_input_box)

        self.button = MyGhostFlatButton(
            center_x=right_column_x+65,
            center_y=(y_slot * 2)+50,
            input_box=ui_input_box
        )
        self.button.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.WHITE,
            font_color_press=arcade.color.WHITE,
            bg_color=(51, 139, 57),
            bg_color_hover=(51, 139, 57),
            bg_color_press=(28, 71, 32),
            border_color=(51, 139, 57),
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )
        self.ui_manager.add_ui_element(self.button)

        self.OutputLabel= arcade.gui.UILabel(
            '',
            center_x=right_column_x+65,
            center_y=(y_slot * 2)-25,
        )
        self.ui_manager.add_ui_element(self.OutputLabel)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        self.grid_sprite_list.draw()
    
    def on_show_view(self):
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        # Change the x/y screen coordinates to grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        #print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row < ROW_COUNT and column < COLUMN_COUNT:

            # Flip the location between 1 and 0.
            if self.grid_sprites[row][column].color == arcade.color.WHITE:
                self.OutputLabel.text='no robot here!'
                self.OutputLabel.color=arcade.color.RED
                pass
                #self.grid_sprites[row][column].color = arcade.color.GREEN
            else:
                self.grid_sprites[row][column].on_tap()
                if self.grid_sprites[row][column].isplayer: return
                self.OutputLabel.text=''
                globals()['selectedbot']=self.grid_sprites[row][column]
                self.window.show_view(RobotView())
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            self.button.on_click()

class RobotView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        global selectedbot
        arcade.start_render()
        for name, val in selectedbot.kernel.__dict__.items():
            if len(str(val))>6: continue
            arcade.draw_text(name+': '+str(val), (SCREEN_WIDTH/6)-30, SCREEN_HEIGHT-(60+(35*list(selectedbot.kernel.__dict__.keys()).index(name))),
                            arcade.color.YELLOW, font_size=18, anchor_x="center") # variable
    
    def on_mouse_press(self, x, y, button, modifiers):
        #self.window.show_view(game)
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(game)
        elif symbol == arcade.key.ENTER:
            game.button.on_click()

window=arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Camillettss')
game=GameView()
window.show_view(game)
arcade.run()
