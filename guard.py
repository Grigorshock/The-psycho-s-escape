import arcade
import math
import constants
import random


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

        self.path = []
        self.current_path_index = 0
        self.repath_timer = 0.0
        self.repath_cooldown = 0.5
        self.stuck_timer = 0.0
        self.stuck_threshold = 1.0
        self.last_positions = []
        self.wander_timer = 0.0
        self.wander_target = None

        self.walk_down_textures = []
        self.walk_up_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []
        self.attack_textures = {}
        self.load_textures()
        self.texture = self.walk_down_textures[0]

        self.move_to_target = None
        self.move_to_complete_callback = None
        self.moving_to_target = False
        self.target = None
        self.speed = self.normal_speed

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

    def find_simple_path(self, target_x, target_y, walls):
        if not walls:
            return [(target_x, target_y)]

        directions = [
            (0, 100), (0, -100), (100, 0), (-100, 0),
            (70, 70), (-70, 70), (70, -70), (-70, -70)
        ]

        best_pos = None
        best_distance = float('inf')

        for dx, dy in directions:
            test_x = self.center_x + dx
            test_y = self.center_y + dy

            if not (20 <= test_x <= constants.SCREEN_WIDTH - 20 and
                    20 <= test_y <= constants.SCREEN_HEIGHT - 20):
                continue

            old_x, old_y = self.center_x, self.center_y
            self.center_x, self.center_y = test_x, test_y
            collision = any(self.collides_with_sprite(wall) for wall in walls)
            self.center_x, self.center_y = old_x, old_y

            if not collision:
                distance_to_target = math.hypot(test_x - target_x, test_y - target_y)
                if distance_to_target < best_distance:
                    best_distance = distance_to_target
                    best_pos = (test_x, test_y)

        if best_pos:
            return [best_pos]

        for dx, dy in directions:
            test_x = self.center_x + dx
            test_y = self.center_y + dy

            if not (20 <= test_x <= constants.SCREEN_WIDTH - 20 and
                    20 <= test_y <= constants.SCREEN_HEIGHT - 20):
                continue

            old_x, old_y = self.center_x, self.center_y
            self.center_x, self.center_y = test_x, test_y
            collision = any(self.collides_with_sprite(wall) for wall in walls)
            self.center_x, self.center_y = old_x, old_y

            if not collision:
                return [(test_x, test_y)]

        return []

    def move_towards_point_smooth(self, target_x, target_y, delta_time, walls):
        dx = target_x - self.center_x
        dy = target_y - self.center_y
        distance = math.hypot(dx, dy)

        if distance < 10:
            self.change_x = 0
            self.change_y = 0
            return True

        if distance > 0:
            ndx = dx / distance
            ndy = dy / distance
        else:
            ndx = 0
            ndy = 0

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

        move_distance = self.current_speed * delta_time
        test_x = self.center_x + ndx * move_distance
        test_y = self.center_y + ndy * move_distance

        old_x, old_y = self.center_x, self.center_y
        self.center_x, self.center_y = test_x, test_y

        collision = False
        for wall in walls:
            if self.collides_with_sprite(wall):
                collision = True
                break

        self.center_x, self.center_y = old_x, old_y

        if not collision:
            self.change_x = ndx * self.current_speed
            self.change_y = ndy * self.current_speed
            return False
        else:
            test_x_only = self.center_x + ndx * move_distance
            test_y_only = self.center_y

            self.center_x, self.center_y = test_x_only, test_y_only
            x_collision = any(self.collides_with_sprite(wall) for wall in walls)
            self.center_x, self.center_y = old_x, old_y

            test_x_only = self.center_x
            test_y_only = self.center_y + ndy * move_distance

            self.center_x, self.center_y = test_x_only, test_y_only
            y_collision = any(self.collides_with_sprite(wall) for wall in walls)
            self.center_x, self.center_y = old_x, old_y

            if not x_collision and not y_collision:
                self.change_x = ndx * self.current_speed
                self.change_y = ndy * self.current_speed
            elif not x_collision:
                self.change_x = ndx * self.current_speed
                self.change_y = 0
            elif not y_collision:
                self.change_x = 0
                self.change_y = ndy * self.current_speed
            else:
                self.change_x = 0
                self.change_y = 0
                return True

        return False

    def update_chase(self, player, delta_time, walls):
        self.current_speed = self.chase_speed

        if player and self.can_see_player(player):
            self.last_seen_player_pos = (player.center_x, player.center_y)
            self.search_timer = 3.0
            self.stuck_timer = 0.0

            self.repath_timer -= delta_time
            if self.repath_timer <= 0 or not self.path:
                self.path = self.find_simple_path(
                    player.center_x, player.center_y, walls
                )
                self.current_path_index = 0
                self.repath_timer = self.repath_cooldown

        if self.last_seen_player_pos:
            target_x, target_y = self.last_seen_player_pos

            if self.path and self.current_path_index < len(self.path):
                next_point = self.path[self.current_path_index]
                reached = self.move_towards_point_smooth(
                    next_point[0], next_point[1], delta_time, walls
                )

                if reached:
                    self.current_path_index += 1
                    if self.current_path_index >= len(self.path):
                        self.path = []
                        self.current_path_index = 0
            else:
                stuck = self.move_towards_point_smooth(target_x, target_y, delta_time, walls)
                if stuck:
                    self.path = self.find_simple_path(target_x, target_y, walls)
                    self.current_path_index = 0

            if player:
                dx = player.center_x - self.center_x
                dy = player.center_y - self.center_y
                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= self.attack_range:
                    self.state = "attack"
                    self.path = []
                    self.change_x = 0
                    self.change_y = 0

    def update_attack(self, player, delta_time):
        if player is None:
            self.state = "chase"
            return

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
        else:
            self.attack_timer -= delta_time

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

        if self.moving_to_target and self.target:
            self.state = "move_to_point"

        if self.state == "idle":
            self.change_x = 0.0
            self.change_y = 0.0
            self.path = []

            if player and self.can_see_player(player):
                self.state = "chase"
                self.last_seen_player_pos = (player.center_x, player.center_y)
                self.path = self.find_simple_path(
                    player.center_x, player.center_y, walls
                )
                self.current_path_index = 0

        elif self.state == "chase":
            self.update_chase(player, delta_time, walls)

            if not self.can_see_player(player):
                self.search_timer -= delta_time
                if self.search_timer <= 0:
                    self.state = "idle"
                    self.path = []
                    self.last_seen_player_pos = None

        elif self.state == "attack":
            self.update_attack(player, delta_time)
        elif self.state == "move_to_point":
            self.update_move_to_point(delta_time, walls)

            if player and self.can_see_player(player):
                self.state = "chase"
                self.last_seen_player_pos = (player.center_x, player.center_y)
                self.moving_to_target = False
                self.target = None
                self.path = self.find_simple_path(
                    player.center_x, player.center_y, walls
                )
                self.current_path_index = 0

        self.update_animation(delta_time)

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        self.center_x = max(20, min(constants.SCREEN_WIDTH - 20, self.center_x))
        self.center_y = max(20, min(constants.SCREEN_HEIGHT - 20, self.center_y))

        if walls:
            collision_occurred = False
            for wall in walls:
                if self.collides_with_sprite(wall):
                    self.center_x = old_x
                    self.center_y = old_y
                    collision_occurred = True

                    if self.state == "chase" and self.last_seen_player_pos:
                        self.repath_timer = 0
                        self.path = self.find_simple_path(
                            self.last_seen_player_pos[0],
                            self.last_seen_player_pos[1],
                            walls
                        )
                        self.current_path_index = 0
                    elif self.state == "move_to_point" and self.target:
                        self.repath_timer = 0
                        self.path = self.find_simple_path(
                            self.target[0],
                            self.target[1],
                            walls
                        )
                        self.current_path_index = 0
                    break

            self.last_positions.append((self.center_x, self.center_y))
            if len(self.last_positions) > 10:
                self.last_positions.pop(0)

            if len(self.last_positions) >= 5:
                first_pos = self.last_positions[0]
                last_pos = self.last_positions[-1]
                distance_moved = math.hypot(
                    last_pos[0] - first_pos[0],
                    last_pos[1] - first_pos[1]
                )

                if distance_moved < 20:
                    self.stuck_timer += delta_time
                    if self.stuck_timer > self.stuck_threshold:
                        self.stuck_timer = 0
                        if self.state == "chase" and self.last_seen_player_pos:
                            self.change_x = random.uniform(-50, 50)
                            self.change_y = random.uniform(-50, 50)
                            self.last_positions = []
                else:
                    self.stuck_timer = 0

    def move_to_point(self, target_x, target_y, walls=None):
        self.target = (target_x, target_y)
        self.moving_to_target = True
        self.state = "move_to_point"

        dx = target_x - self.center_x
        dy = target_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 100:
            self.center_x = target_x
            self.center_y = target_y
            self.change_x = 0
            self.change_y = 0
            self.moving_to_target = False
            self.state = "idle"
            print(f"Охранник телепортирован к {target_x}, {target_y}")
        else:
            self.path = []
            self.current_path_index = 0
            self.repath_timer = 0
            self.current_speed = self.normal_speed
            print(f"Охранник идет к {target_x}, {target_y}")

    def update_move_to_point(self, delta_time, walls):
        if not self.target:
            self.state = "idle"
            self.moving_to_target = False
            return

        self.current_speed = self.normal_speed

        target_x, target_y = self.target
        dx = target_x - self.center_x
        dy = target_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 30:
            self.change_x = 0
            self.change_y = 0
            self.state = "idle"
            self.moving_to_target = False
            self.target = None
            print("Охранник достиг цели")
            return

        if distance < 100:
            self.change_x = 0
            self.change_y = 0
            self.center_x = target_x
            self.center_y = target_y
            self.state = "idle"
            self.moving_to_target = False
            self.target = None
            print("Охранник телепортирован (близкая цель)")
            return

        self.repath_timer -= delta_time
        if self.repath_timer <= 0 or not self.path:
            self.path = self.find_simple_path(target_x, target_y, walls)
            self.current_path_index = 0
            self.repath_timer = self.repath_cooldown

        if self.path and self.current_path_index < len(self.path):
            next_point = self.path[self.current_path_index]
            reached = self.move_towards_point_smooth(
                next_point[0], next_point[1], delta_time, walls
            )

            if reached:
                self.current_path_index += 1
                if self.current_path_index >= len(self.path):
                    self.path = []
                    self.current_path_index = 0
        else:
            reached = self.move_towards_point_smooth(target_x, target_y, delta_time, walls)
            if reached:
                self.change_x = 0
                self.change_y = 0
                self.state = "idle"
                self.moving_to_target = False
                self.target = None
                print("Охранник не может дойти до цели")

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