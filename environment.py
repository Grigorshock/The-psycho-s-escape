# комнаты
import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Floor(arcade.Sprite):
    def __init__(self, imag, x, y):
        super().__init__(imag, 0.67, x, y)

class Wall(arcade.Sprite):
    def __init__(self, imag, x, y):
        super().__init__(imag, 0.457, x, y)