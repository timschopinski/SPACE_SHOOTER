import pygame_menu
from screen import Screen




class Menu(pygame_menu.Menu):
    def __init__(self, x, y, theme=Screen.MY_THEME):
        self.x = x
        self.y = y
        self.theme = theme
        self.menu = pygame_menu.Menu('',self.x, self.y, theme=self.theme)
        self.set_highlight()

    def display_menu(self, function1, function2, function3, function4, surface):
        self.menu.add.text_input(f'NAME: ', default='', onreturn=function1)
        self.menu.add.selector('Difficulty :', [('Easy', 1), ('Hard', 2)], onchange=function2)
        self.menu.add.button('Play', function3)
        self.menu.add.button('Scoreboard', function4)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)


    def set_highlight(self):
        pygame_menu.widgets.HighlightSelection(border_width=1, margin_x=16, margin_y=8)
