import arcade
import constants
from environment import Part_environment, Door


class Room1:
    def __init__(self):
        self.all_textures_room = arcade.SpriteList()
        self.walls = arcade.SpriteList()

        env = Part_environment("images\\окружение\\стена_справо.png", 0.457, 646, 300)
        self.walls.append(env)
        self.all_textures_room.append(env)

        env = Part_environment("images\\окружение\\стена_сверху.png", 0.457, 400, 547)
        self.walls.append(env)
        self.all_textures_room.append(env)

        env = Part_environment("images\\окружение\\стена_снизу.png", 0.457, 400, 53)
        self.walls.append(env)
        self.all_textures_room.append(env)

        env = Part_environment("images\\окружение\\стена_слева.png", 0.457, 153, 300)
        self.walls.append(env)
        self.all_textures_room.append(env)

        # пол
        env = Part_environment("images\\окружение\\пол.png", 0.67,
                               constants.SCREEN_WIDTH // 2,
                               constants.SCREEN_HEIGHT // 2)
        self.all_textures_room.append(env)

        self.door = Door("images\\окружение\\дверь.png", 0.36, 619, 277, 1, [550, 290])
        self.all_textures_room.append(self.door)


class Room2:
    def __init__(self):
        self.all_textures_room = arcade.SpriteList()
        self.walls = arcade.SpriteList()


        env = Part_environment("images\\окружение\\пол_к2.png", 0.2, 300, 230)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\пол_к2.png", 0.2, 300, 360)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\пол_к2.png", 0.2, 300, 490)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\пол_к2.png", 0.2, 475, 230)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\пол_к2.png", 0.2, 475, 360)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\пол_к2.png", 0.2, 475, 490)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\пол_к2.png", 0.2, 650, 230)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\пол_к2.png", 0.2, 650, 360)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\пол_к2.png", 0.2, 650, 490)
        self.all_textures_room.append(env)

        env = Part_environment("images\\окружение\\пятно.png", 0.4, 350, 420)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\стул.png", 0.4, 370, 435)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стол.png", 0.4, 355, 490)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\телефон.png", 0.2, 340, 495)
        self.all_textures_room.append(env)
        self.walls.append(env)

        env = Part_environment("images\\окружение\\стена_к2.png", 0.4, 765, 225)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к2.png", 0.4, 765, 340)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к2.png", 0.4, 765, 495)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к2.png", 0.4, 765, 410)
        self.all_textures_room.append(env)
        self.walls.append(env)

        env = Part_environment("images\\окружение\\стена_к2.png", 0.4, 200, 225)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к2.png", 0.4, 200, 340)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к2.png", 0.4, 200, 495)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к2.png", 0.4, 200, 410)
        self.all_textures_room.append(env)
        self.walls.append(env)

        env = Part_environment("images\\окружение\\стена_к22.png", 0.4, 285, 570)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к22.png", 0.4, 405, 570)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к22.png", 0.4, 520, 570)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к22.png", 0.4, 680, 570)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к22.png", 0.4, 570, 570)
        self.all_textures_room.append(env)
        self.walls.append(env)

        env = Part_environment("images\\окружение\\стена_к22.png", 0.4, 285, 135)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к22.png", 0.4, 405, 135)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к22.png", 0.4, 520, 135)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к22.png", 0.4, 680, 135)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к22.png", 0.4, 570, 135)
        self.all_textures_room.append(env)
        self.walls.append(env)

        env = Part_environment("images\\окружение\\угл1.png", 0.4, 767, 569)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\угл4.png", 0.4, 200, 570)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\угл3.png", 0.4, 765, 136)
        self.all_textures_room.append(env)
        env = Part_environment("images\\окружение\\угл2.png", 0.4, 202, 136)
        self.all_textures_room.append(env)

        env = Part_environment("images\\окружение\\стена_к222.png", 0.4, 680, 400)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\стена_к2222.png", 0.4, 580, 399)
        self.all_textures_room.append(env)
        self.walls.append(env)
        env = Part_environment("images\\окружение\\угл2.png", 0.4, 530, 402)
        self.all_textures_room.append(env)


        self.door = Door("images\\окружение\\дверь_в_1к.png", 1.3, 380, 120, 0, [380, 205])
        self.all_textures_room.append(self.door)

        self.door2 = Door("images\\окружение\\дверь_финал.png", 0.2, 750, 300, 0, [0, 0])
        self.all_textures_room.append(self.door2)
