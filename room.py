import arcade
from environment import Part_environment, Door
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Room1(arcade.Sprite):
    def __init__(self):
        super().__init__(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.all_textures_room = arcade.SpriteList()
        self.walls = arcade.SpriteList()

        environment = Part_environment("images\окружение\стена_справо.png", 0.457, 646, 300)
        self.walls.append(environment)
        self.all_textures_room.append(environment)

        environment = Part_environment("images\окружение\стена_сверху.png", 0.457, 400, 547)
        self.walls.append(environment)
        self.all_textures_room.append(environment)

        environment = Part_environment("images\окружение\стена_снизу.png", 0.457, 400, 53)
        self.walls.append(environment)
        self.all_textures_room.append(environment)

        environment = Part_environment("images\окружение\стена_слева.png", 0.457, 153, 300)
        self.walls.append(environment)
        self.all_textures_room.append(environment)

        environment = Part_environment("images\окружение\пол.png", 0.67, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # пол
        self.all_textures_room.append(environment)

        self.door = Door("images\окружение\дверь.png", 0.36, 619, 277, 1)
        self.all_textures_room.append(self.door)


class Room2(arcade.Sprite):
    def __init__(self):
        super().__init__(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.all_textures_room = arcade.SpriteList()
        self.walls = arcade.SpriteList()

        environment = Part_environment("images\окружение\стена_справо.png", 0.457, 646, 300)
        self.walls.append(environment)
        self.all_textures_room.append(environment)

        environment = Part_environment("images\окружение\пол_2.png", 1.5, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_textures_room.append(environment)

        self.door = Door("images\окружение\дверь_3.png", 1, 621, 277, 0)
        self.all_textures_room.append(self.door)