import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Psycho(arcade.Sprite):
    def __init__(self):
        super().__init__("images\перс1-removebg-preview.png", 0.5)

        self.hp = 100

        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

        self.change_x = 0
        self.change_y = 0
        self.normal_speed = 2
        self.shift_speed = 3
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
                f"images\перс{i}-removebg-preview.png")
            self.walk_down_textures.append(texture)

        for i in [3, 4]:
            texture = arcade.load_texture(
                f"images\перс{i}-removebg-preview.png")
            self.walk_up_textures.append(texture)

        for i in [5, 6]:
            texture = arcade.load_texture(
                f"images\перс{i}-removebg-preview.png")
            self.walk_right_textures.append(texture)

        for i in [7, 8]:
            texture = arcade.load_texture(
                f"images\перс{i}-removebg-preview.png")
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
    def take_damage(self, damage):
        self.hp -= damage
        print(f"{self.hp}хп")
