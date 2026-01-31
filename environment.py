import arcade

class Part_environment(arcade.Sprite):
    def __init__(self, imag, scale, x, y):
        super().__init__(imag, scale, x, y)

class Door(arcade.Sprite):
    def __init__(self, imag, scale, x, y, next_room, spawn_coordinates):
        super().__init__(imag, scale, x, y)
        self.next_room = next_room
        self.spawn_coordinates = spawn_coordinates