import arcade
from environment import Floor, Wall
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Room1(arcade.Sprite):
    def __init__(self):
        super().__init__(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.all_textures_room = arcade.SpriteList()
        self.walls = arcade.SpriteList()

        environment = Wall("images\окружение\стена_справо.png", 647, 300)
        self.walls.append(environment)
        self.all_textures_room.append(environment)

        environment = Wall("images\окружение\стена_сверху.png", 400, 547)
        self.walls.append(environment)
        self.all_textures_room.append(environment)

        environment = Wall("images\окружение\стена_слева.png", 153, 300)
        self.walls.append(environment)
        self.all_textures_room.append(environment)

        environment = Wall("images\окружение\стена_снизу.png", 400, 53)
        self.walls.append(environment)
        self.all_textures_room.append(environment)

        environment = Floor("images\окружение\пол.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_textures_room.append(environment)