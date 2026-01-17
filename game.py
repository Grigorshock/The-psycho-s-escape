import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The psycho escape"


class Psycho(arcade.Sprite):
    def __init__(self):
        super().__init__("C:\\Users\\Грига\\PycharmProjects\\Arcade\\images\\перс1-removebg-preview.png", 0.5)

        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

        self.change_x = 0
        self.change_y = 0
        self.normal_speed = 250
        self.shift_speed = 350
        self.current_speed = self.normal_speed

        self.animation_timer = 0
        self.animation_speed = 0.20
        self.current_frame = 0

        self.walk_down_textures = []
        self.walk_up_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []

        for i in [1, 2]:
            texture = arcade.load_texture(
                f"C:\\Users\\Грига\\PycharmProjects\\Arcade\\images\\перс{i}-removebg-preview.png")
            self.walk_down_textures.append(texture)

        for i in [3, 4]:
            texture = arcade.load_texture(
                f"C:\\Users\\Грига\\PycharmProjects\\Arcade\\images\\перс{i}-removebg-preview.png")
            self.walk_up_textures.append(texture)

        for i in [5, 6]:
            texture = arcade.load_texture(
                f"C:\\Users\\Грига\\PycharmProjects\\Arcade\\images\\перс{i}-removebg-preview.png")
            self.walk_right_textures.append(texture)

        for i in [7, 8]:
            texture = arcade.load_texture(
                f"C:\\Users\\Грига\\PycharmProjects\\Arcade\\images\\перс{i}-removebg-preview.png")
            self.walk_left_textures.append(texture)

        self.texture = self.walk_down_textures[0]

        self.facing_direction = "down"

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.bottom < 0:
            self.bottom = 0
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT

        if self.change_x != 0 or self.change_y != 0:
            self.animation_timer += delta_time

            if abs(self.change_y) > abs(self.change_x):
                if self.change_y > 0:
                    self.facing_direction = "up"
                    current_textures = self.walk_up_textures
                else:
                    self.facing_direction = "down"
                    current_textures = self.walk_down_textures
            else:
                if self.change_x > 0:
                    self.facing_direction = "right"
                    current_textures = self.walk_right_textures
                else:
                    self.facing_direction = "left"
                    current_textures = self.walk_left_textures

            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % 2
                self.texture = current_textures[self.current_frame]
        else:
            self.current_frame = 0
            if self.facing_direction == "up":
                self.texture = self.walk_up_textures[0]
            elif self.facing_direction == "down":
                self.texture = self.walk_down_textures[0]
            elif self.facing_direction == "right":
                self.texture = self.walk_right_textures[0]
            elif self.facing_direction == "left":
                self.texture = self.walk_left_textures[0]


class Room(arcade.Sprite):
    def __init__(self):
        super().__init__("images\пол.png", 0.67, SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT // 2)

class Wall(arcade.Sprite):
    def __init__(self):
        super().__init__("C:\\Users\Грига\PycharmProjects\Arcade\images\стена(палата).png", 0.6, 720, 300)


class The_psycho_escape(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        self.psycho = Psycho()
        self.psycho_list = arcade.SpriteList()
        self.psycho_list.append(self.psycho)

        self.stool = Wall()
        self.stool_list = arcade.SpriteList()
        self.stool_list.append(self.stool)

        self.room = Room()
        self.room_list = arcade.SpriteList()
        self.room_list.append(self.room)

    def on_draw(self):
        self.clear()

        self.room_list.draw()
        self.stool_list.draw()
        self.psycho_list.draw()

    def on_update(self, delta_time):
        self.psycho.update(delta_time)
        is_collision = arcade.check_for_collision(self.psycho, self.stool)
        if is_collision:
            pass # TODO если вр езался в стену

    def on_key_press(self, key, modifiers):
        if modifiers & arcade.key.MOD_SHIFT:
            self.psycho.current_speed = self.psycho.shift_speed
        else:
            self.psycho.current_speed = self.psycho.normal_speed

        if key == arcade.key.UP or key == arcade.key.W:
            self.psycho.change_y = self.psycho.current_speed
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.psycho.change_y = -self.psycho.current_speed

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.psycho.change_x = -self.psycho.current_speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.psycho.change_x = self.psycho.current_speed

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.psycho.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.psycho.change_x = 0

        if not (modifiers & arcade.key.MOD_SHIFT):
            self.psycho.current_speed = self.psycho.normal_speed


def main():
    game = The_psycho_escape(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
