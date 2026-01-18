import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Room(arcade.Sprite):
    def __init__(self):
        super().__init__("images\пол.png", 0.67, SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT // 2)