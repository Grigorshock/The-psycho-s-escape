import arcade
import constants


class Psycho(arcade.Sprite):
    def __init__(self, camera, x=400, y=300):
        super().__init__("images/игрок_ходьба/стоит_вниз.png", 1)
        self.stun_timer = 0.0
        self.stun_duration = 0.5
        self.center_x = x
        self.center_y = y
        self.camera = camera
        self.hp = 100
        self.damage_timer = 0
        self.damage_cooldown = 1.0
        self.walk_down_textures = []
        self.walk_up_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.20
        self.facing_direction = "down"
        self.is_falling = False
        self.fall_timer = 0.0
        self.fall_duration = 1.0
        self.fall_frame_duration = 0.2
        self.current_fall_frame = 0
        self.current_speed = 180.0
        self.load_textures()

    def load_textures(self):
        for i in range(1, 9):
            self.walk_down_textures.append(arcade.load_texture(f"images/игрок_ходьба/идёт_вниз_{i}.png"))
            self.walk_up_textures.append(arcade.load_texture(f"images/игрок_ходьба/идёт_вверх_{i}.png"))
        for i in range(1, 6):
            self.walk_right_textures.append(arcade.load_texture(f"images/игрок_ходьба/идёт_вправо_{i}.png"))
            self.walk_left_textures.append(arcade.load_texture(f"images/игрок_ходьба/идёт_влево_{i}.png"))
        self.stand_texture = arcade.load_texture("images/игрок_ходьба/стоит_вниз.png")
        self.fall_textures = [
            arcade.load_texture("images/игрок_ходьба/упал_1.png"),
            arcade.load_texture("images/игрок_ходьба/упал_2.png"),
            arcade.load_texture("images/игрок_ходьба/упал_3.png"),
            arcade.load_texture("images/игрок_ходьба/упал_4.png"),
            arcade.load_texture("images/игрок_ходьба/упал_5.png"),
        ]

    def update(self, delta_time: float):
        if self.is_falling:
            self.update_fall_animation(delta_time)
            return

        if self.stun_timer > 0:
            self.stun_timer -= delta_time
            self.change_x = 0
            self.change_y = 0

        if self.damage_timer > 0:
            self.damage_timer -= delta_time

        self.center_x += self.change_x * self.current_speed * delta_time
        self.center_y += self.change_y * self.current_speed * delta_time

        if self.left < 0:
            self.left = 0
        if self.right > constants.SCREEN_WIDTH:
            self.right = constants.SCREEN_WIDTH
        if self.bottom < 0:
            self.bottom = 0
        if self.top > constants.SCREEN_HEIGHT:
            self.top = constants.SCREEN_HEIGHT

        self.update_animation(delta_time)

    def update_fall_animation(self, delta_time: float):
        self.fall_timer += delta_time

        self.animation_timer += delta_time
        if self.animation_timer >= self.fall_frame_duration:
            self.animation_timer = 0.0
            self.current_fall_frame += 1

            if self.current_fall_frame >= len(self.fall_textures):
                self.current_fall_frame = len(self.fall_textures) - 1

            self.texture = self.fall_textures[self.current_fall_frame]

        if self.fall_timer >= self.fall_duration:
            self.is_falling = False
            self.fall_timer = 0.0
            self.current_fall_frame = 0
            self.texture = self.stand_texture

    def update_animation(self, delta_time: float):
        moving = (self.change_x != 0) or (self.change_y != 0)

        if moving:
            self.animation_timer += delta_time

            if abs(self.change_x) > abs(self.change_y):
                self.facing_direction = "right" if self.change_x > 0 else "left"
            else:
                self.facing_direction = "up" if self.change_y > 0 else "down"

            if self.facing_direction == "up":
                current_textures = self.walk_up_textures
            elif self.facing_direction == "down":
                current_textures = self.walk_down_textures
            elif self.facing_direction == "right":
                current_textures = self.walk_right_textures
            else:
                current_textures = self.walk_left_textures

            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0.0
                self.current_frame = (self.current_frame + 1) % len(current_textures)
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
            else:
                self.texture = self.stand_texture

    def take_damage(self, damage: int) -> bool:
        if self.damage_timer > 0 or self.is_falling:
            return False

        self.hp -= damage
        self.damage_timer = self.damage_cooldown

        self.stun_timer = self.stun_duration
        self.change_x = 0
        self.change_y = 0

        print(f"Игрок HP: {self.hp}")

        if self.hp <= 0:
            self.fall_down()

        self.fall_down()

        return True

    def fall_down(self):
        self.is_falling = True
        self.fall_timer = 0.0
        self.current_fall_frame = 0
        self.animation_timer = 0.0
        if self.fall_textures:
            self.texture = self.fall_textures[0]

    def on_key_press(self, key):
        if self.is_falling or self.stun_timer > 0:
            return

        if key == arcade.key.W:
            self.change_y = 1
        elif key == arcade.key.S:
            self.change_y = -1
        elif key == arcade.key.A:
            self.change_x = -1
        elif key == arcade.key.D:
            self.change_x = 1

    def on_key_release(self, key):
        if key in (arcade.key.W, arcade.key.S):
            self.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.change_x = 0