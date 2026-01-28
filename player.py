import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Psycho(arcade.Sprite):
    def __init__(self):
        super().__init__(r"images\игрок_ходьба\идёт_вниз_1.png", 1)

        self.hp = 100

        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

        self.change_x = 0
        self.change_y = 0
        self.normal_speed = 1
        self.shift_speed = 1.5
        self.current_speed = self.normal_speed

        self.animation_timer = 0
        self.animation_speed = 0.15
        self.current_frame = 0

        self.walk_down_textures = []
        self.walk_up_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []
        self.stands_still = []
        self.fell = []

        self.is_taking_damage = False
        self.damage_animation_timer = 0
        self.damage_animation_duration = 1.0
        self.damage_frame_duration = 0

        self.is_dead = False
        self.death_animation_timer = 0
        self.death_animation_duration = 2.0
        self.death_frame_duration = 0

        texture = arcade.load_texture(r"images\игрок_ходьба\стоит_вниз.png")
        self.stands_still.append(texture)
        texture = arcade.load_texture(r"images\игрок_ходьба\стоит_вверх.png")
        self.stands_still.append(texture)
        texture = arcade.load_texture(r"images\игрок_ходьба\стоит_вправо.png")
        self.stands_still.append(texture)
        texture = arcade.load_texture(r"images\игрок_ходьба\стоит_влево.png")
        self.stands_still.append(texture)

        for i in range(1, 8):
            texture = arcade.load_texture(rf"images\игрок_ходьба\идёт_вниз_{i}.png")
            self.walk_down_textures.append(texture)

        for i in range(1, 8):
            texture = arcade.load_texture(rf"images\игрок_ходьба\идёт_вверх_{i}.png")
            self.walk_up_textures.append(texture)

        for i in range(1, 5):
            texture = arcade.load_texture(rf"images\игрок_ходьба\идёт_вправо_{i}.png")
            self.walk_right_textures.append(texture)

        for i in range(1, 8):
            texture = arcade.load_texture(rf"images\игрок_ходьба\идёт_влево_{i}.png")
            self.walk_left_textures.append(texture)

        for i in range(1, 5):
            texture = arcade.load_texture(rf"images\игрок_ходьба\упал_{i}.png")
            self.fell.append(texture)

        self.texture = self.stands_still[0]
        self.facing_direction = "down"

    def update(self, delta_time):
        if self.is_dead:
            self.death_animation_timer += delta_time
            self.death_frame_duration += delta_time

            total_frames = len(self.fell)
            frame_duration = self.death_animation_duration / total_frames

            if self.death_frame_duration >= frame_duration and self.death_animation_timer < self.death_animation_duration:
                self.death_frame_duration = 0
                self.current_frame = min(
                    int(self.death_animation_timer / frame_duration),
                    total_frames - 1
                )
                self.texture = self.fell[self.current_frame]

            self.change_x = 0
            self.change_y = 0
            return

        if self.is_taking_damage:
            self.damage_animation_timer += delta_time
            self.damage_frame_duration += delta_time

            total_frames = len(self.fell)
            frame_duration = self.damage_animation_duration / total_frames

            if self.damage_frame_duration >= frame_duration:
                self.damage_frame_duration = 0
                self.current_frame = min(
                    int(self.damage_animation_timer / frame_duration),
                    total_frames - 1
                )
                self.texture = self.fell[self.current_frame]

            if self.damage_animation_timer >= self.damage_animation_duration:
                self.is_taking_damage = False
                self.damage_animation_timer = 0
                self.current_frame = 0
                self.damage_frame_duration = 0
                if self.facing_direction == "up":
                    self.texture = self.stands_still[1]
                elif self.facing_direction == "down":
                    self.texture = self.stands_still[0]
                elif self.facing_direction == "right":
                    self.texture = self.stands_still[2]
                elif self.facing_direction == "left":
                    self.texture = self.stands_still[3]

        if not self.is_taking_damage and not self.is_dead:
            self.center_x += self.change_x * self.current_speed
            self.center_y += self.change_y * self.current_speed

        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.bottom < 0:
            self.bottom = 0
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT

        if not self.is_taking_damage and not self.is_dead and (self.change_x != 0 or self.change_y != 0):
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
                self.current_frame = (self.current_frame + 1) % len(current_textures)
                self.texture = current_textures[self.current_frame]
        elif not self.is_taking_damage and not self.is_dead and (self.change_x == 0 and self.change_y == 0):
            self.current_frame = 0
            if self.facing_direction == "up":
                self.texture = self.stands_still[1]
            elif self.facing_direction == "down":
                self.texture = self.stands_still[0]
            elif self.facing_direction == "right":
                self.texture = self.stands_still[2]
            elif self.facing_direction == "left":
                self.texture = self.stands_still[3]

    def take_damage(self, damage):
        self.hp -= damage
        print(f"{self.hp} хп")

        if self.hp <= 0 and not self.is_dead:
            self.die()
            return

        self.is_taking_damage = True
        self.damage_animation_timer = 0
        self.damage_frame_duration = 0
        self.current_frame = 0
        self.animation_timer = 0

    def die(self):
        if not self.is_dead:
            self.is_dead = True
            self.is_taking_damage = False
            self.change_x = 0
            self.change_y = 0
            self.death_animation_timer = 0
            self.death_frame_duration = 0
            self.current_frame = 0
            self.texture = self.fell[0]