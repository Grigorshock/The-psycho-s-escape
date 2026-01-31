# комнаты
import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Part_environment(arcade.Sprite):
    def __init__(self, imag, w, x, y):
        super().__init__(imag, w, x, y)

class Door(arcade.Sprite):
    def __init__(self, imag, w, x, y, next_room):
        super().__init__(imag, w, x, y)
        self.next_room = next_room