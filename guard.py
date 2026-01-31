import arcade
import math
import constants


class Guard(arcade.Sprite):
    def __init__(self, patrol_points=None):
        super().__init__("images/охранник/Guard_down1.png")
        self.scale = 0.5
        self.hp = 100
        self.change_x = 0.0
        self.change_y = 0.0
        self.normal_speed = 120.0
        self.chase_speed = 200.0
        self.current_speed = self.normal_speed
        self.animation_timer = 0.0
        self.animation_speed = 0.20
        self.current_frame = 0
        self.facing_direction = "down"
        self.state = "idle"
        self.last_seen_player_pos = None
        self.search_timer = 0.0
        self.attack_timer = 0.0
        self.view_distance = 300
        self.view_angle = 90
        self.attack_range = 50
        self.attack_cooldown = 1.5
        self.attack_damage = 25
        self.attack_animation_time = 0.3
        self.attack_animation_timer = 0.0
        self.walk_down_textures = []
        self.walk_up_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []
        self.attack_textures = {}
        self.load_textures()
        self.texture = self.walk_down_textures[0]

    def load_textures(self):
        for i in (1, 2):
            self.walk_down_textures.append(arcade.load_texture(f"images/охранник/Guard_down{i}.png"))
        for i in (1, 2):
            self.walk_up_textures.append(arcade.load_texture(f"images/охранник/Guard_up{i}.png"))
        for i in (1, 2):
            self.walk_right_textures.append(arcade.load_texture(f"images/охранник/Guard_right{i}.png"))
        for i in (1, 2):
            self.walk_left_textures.append(arcade.load_texture(f"images/охранник/Guard_left{i}.png"))
        self.attack_textures["down"] = arcade.load_texture("images/охранник/Guard_down_attack.png")
        self.attack_textures["up"] = arcade.load_texture("images/охранник/Guard_up_attack.png")
        self.attack_textures["right"] = arcade.load_texture("images/охранник/Guard_right_attack.png")
        self.attack_textures["left"] = arcade.load_texture("images/охранник/Guard_left_attack.png")

    def can_see_player(self, player):
        if player is None:
            return False
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > self.view_distance:
            return False
        guard_angle = self.get_facing_angle()
        player_angle = math.degrees(math.atan2(dy, dx))
        if player_angle < 0:
            player_angle += 360
        angle_diff = abs(player_angle - guard_angle)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        return angle_diff <= self.view_angle / 2

    def get_facing_angle(self):
        directions = {"right": 0, "up": 90, "left": 180, "down": 270}
        return directions.get(self.facing_direction, 0)

    def move_towards(self, target_x, target_y, delta_time, walls=None):
        dx = target_x - self.center_x
        dy = target_y - self.center_y
        distance = math.hypot(dx, dy)
        if distance == 0:
            self.change_x = 0
            self.change_y = 0
            return
        ndx = dx / distance
        ndy = dy / distance

        if abs(ndx) > abs(ndy):
            if ndx > 0:
                self.facing_direction = "right"
            else:
                self.facing_direction = "left"
        else:
            if ndy > 0:
                self.facing_direction = "up"
            else:
                self.facing_direction = "down"

        for vx, vy in [(ndx, ndy), (ndx, 0), (0, ndy), (ndy, -ndx), (-ndy, ndx)]:
            test_x = self.center_x + vx * self.current_speed * delta_time
            test_y = self.center_y + vy * self.current_speed * delta_time
            blocked = False
            if walls:
                old_x, old_y = self.center_x, self.center_y
                self.center_x, self.center_y = test_x, test_y
                for wall in walls:
                    if self.collides_with_sprite(wall):
                        blocked = True
                        break
                self.center_x, self.center_y = old_x, old_y
            if not blocked:
                self.change_x = vx * self.current_speed
                self.change_y = vy * self.current_speed
                return
        self.change_x = 0
        self.change_y = 0

    def update_chase(self, player, delta_time, walls=None):
        self.current_speed = self.chase_speed
        if player and self.can_see_player(player):
            self.last_seen_player_pos = (player.center_x, player.center_y)
            self.search_timer = 3.0
        if self.last_seen_player_pos:
            tx, ty = self.last_seen_player_pos
            self.move_towards(tx, ty, delta_time, walls)
            if player:
                dx = player.center_x - self.center_x
                dy = player.center_y - self.center_y
                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= self.attack_range:
                    self.state = "attack"

    def update_attack(self, player, delta_time):
        if player is None:
            self.state = "chase"
            return
        if self.attack_timer > 0:
            self.attack_timer -= delta_time
        if self.attack_animation_timer > 0:
            self.attack_animation_timer -= delta_time
            if self.attack_animation_timer <= 0:
                self.update_animation(0)
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > self.attack_range:
            self.state = "chase"
            return
        if self.attack_timer <= 0:
            did_hit = player.take_damage(self.attack_damage)
            if did_hit:
                if hasattr(player, "camera") and player.camera:
                    if hasattr(player.camera, "hit_shake"):
                        player.camera.hit_shake()
            self.attack_timer = self.attack_cooldown
            self.attack_animation_timer = self.attack_animation_time
            self.texture = self.attack_textures.get(self.facing_direction, self.texture)
        self.change_x = 0.0
        self.change_y = 0.0

    def update_animation(self, delta_time):
        if self.attack_animation_timer > 0:
            return
        moving = (self.change_x != 0) or (self.change_y != 0)
        if moving:
            self.animation_timer += delta_time
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

    def update(self, delta_time, player=None, walls=None):
        old_x = self.center_x
        old_y = self.center_y
        if self.state == "idle":
            self.change_x = 0.0
            self.change_y = 0.0
            if player and self.can_see_player(player):
                self.state = "chase"
                self.last_seen_player_pos = (player.center_x, player.center_y)
        elif self.state == "chase":
            if player:
                self.update_chase(player, delta_time, walls)
                if not self.can_see_player(player):
                    self.search_timer -= delta_time
                    if self.search_timer <= 0:
                        self.state = "idle"
        elif self.state == "attack":
            self.update_attack(player, delta_time)
        self.update_animation(delta_time)
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        self.center_x = max(0, min(constants.SCREEN_WIDTH, self.center_x))
        self.center_y = max(0, min(constants.SCREEN_HEIGHT, self.center_y))
        if walls:
            for wall in walls:
                if self.collides_with_sprite(wall):
                    self.center_x = old_x
                    self.center_y = old_y
                    break

    def draw_vision_cone(self):
        angle = self.get_facing_angle()
        half_angle = self.view_angle / 2
        start_angle = math.radians(angle - half_angle)
        end_angle = math.radians(angle + half_angle)
        points = [(self.center_x, self.center_y)]
        for i in range(11):
            current_angle = start_angle + (end_angle - start_angle) * i / 10
            x = self.center_x + math.cos(current_angle) * self.view_distance
            y = self.center_y + math.sin(current_angle) * self.view_distance
            points.append((x, y))
        arcade.draw_polygon_filled(points, (221, 221, 0, 30))