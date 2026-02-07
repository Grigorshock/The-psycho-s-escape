import arcade
import math


class Part_environment(arcade.Sprite):
    def __init__(self, imag, scale, x, y):
        super().__init__(imag, scale, x, y)


class Door(arcade.Sprite):
    def __init__(self, imag, scale, x, y, next_room, spawn_coordinates, spawn_guard=[630, 490]):
        super().__init__(imag, scale, x, y)
        self.next_room = next_room
        self.spawn_coordinates = spawn_coordinates
        self.spawn_guard = spawn_guard


class Phone(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("images\\окружение\\телефон.png", 0.2)
        self.center_x = x
        self.center_y = y
        self.is_ringing = False
        self.ring_timer = 0.0
        self.ring_duration = 3.0
        self.activated = False
        self.interaction_range = 80

        self.ring_animation_timer = 0.0
        self.ring_animation_speed = 10.0
        self.original_scale = 0.2

        self.ring_sound = None
        self.current_sound_instance = None
        self.ring_sound = arcade.load_sound("images\звонок.wav")

    def activate(self):
        if self.activated:
            return False

        self.is_ringing = True
        self.ring_timer = self.ring_duration
        self.activated = True
        self.ring_animation_timer = 0.0

        self.current_sound_instance = arcade.play_sound(
            self.ring_sound,
            volume=0.5,
            loop=True)

        return True

    def update(self, delta_time):
        if self.is_ringing:
            self.ring_timer -= delta_time

            self.ring_animation_timer += delta_time * self.ring_animation_speed
            vibration = 0.02 * abs(abs((self.ring_animation_timer % 2) - 1) - 0.5)
            self.scale = self.original_scale + vibration

            if self.ring_timer <= 0:
                self.stop_ringing()

    def stop_ringing(self):
        if not self.is_ringing:
            return

        self.is_ringing = False
        self.scale = self.original_scale

        if self.current_sound_instance:
            arcade.stop_sound(self.current_sound_instance)
            self.current_sound_instance = None

    def is_player_near(self, player):
        if not player:
            return False

        dx = self.center_x - player.center_x
        dy = self.center_y - player.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        return distance < self.interaction_range

    def draw_hint(self, player):
        if not self.is_player_near(player):
            return

        if not self.activated:
            text = "Позвонить [E]"
            color = arcade.color.WHITE
        elif self.is_ringing:
            text = "Звонит..."
            color = arcade.color.YELLOW
        else:
            text = "Уже звонил"
            color = arcade.color.GRAY

        self.hint_text = arcade.Text(
            text, self.center_x - 110, self.center_y + 115,
            color, 14, bold=True,
            anchor_x="center", anchor_y="center")

        self.hint_text.draw()


class FinalDoor(Door):
    def __init__(self, imag, scale, x, y, next_room, spawn_coordinates, spawn_guard=[630, 490]):
        super().__init__(imag, scale, x, y, next_room, spawn_coordinates, spawn_guard)
        self.interaction_range = 80
        self.interaction_timer = 0.0
        self.interaction_duration = 3.0
        self.is_interacting = False
        self.interaction_start_time = 0.0

    def start_interaction(self):
        if not self.is_interacting:
            self.is_interacting = True
            self.interaction_start_time = 0.0
            return True
        return False

    def update_interaction(self, delta_time, player, guard):
        if not self.is_interacting:
            return False

        self.interaction_start_time += delta_time

        if guard and guard.state == "attack":
            self.is_interacting = False
            self.interaction_start_time = 0.0
            return False

        if not self.is_player_near(player):
            self.is_interacting = False
            self.interaction_start_time = 0.0
            return False

        if self.interaction_start_time >= self.interaction_duration:
            self.is_interacting = False
            return True

        return False

    def cancel_interaction(self):
        self.is_interacting = False
        self.interaction_start_time = 0.0

    def is_player_near(self, player):
        if not player:
            return False
        dx = self.center_x - player.center_x
        dy = self.center_y - player.center_y
        distance = (dx * dx + dy * dy) ** 0.5
        return distance < self.interaction_range

    def draw_hint(self, player):
        if not self.is_player_near(player):
            return

        if self.is_interacting:
            progress = min(self.interaction_start_time / self.interaction_duration, 1.0)
            text = f"Открывается... {progress * 100:.0f}%"
            color = arcade.color.YELLOW
        else:
            text = "Удерживайте [E]"
            color = arcade.color.WHITE

        self.hint_text = arcade.Text(text, self.center_x - 90, self.center_y - 200, color, 14, bold=True,
                                     anchor_x="center", anchor_y="center")
        self.hint_text.draw()
