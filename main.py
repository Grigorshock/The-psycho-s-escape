import arcade
import constants

from psycho import Psycho
from room import Room1, Room2, Final
from guard import Guard
from Camera import camera


class The_psycho_escape(arcade.Window):
    def __init__(self):
        w = getattr(constants, "WINDOW_WIDTH", constants.SCREEN_WIDTH)
        h = getattr(constants, "WINDOW_HEIGHT", constants.SCREEN_HEIGHT)

        super().__init__(w, h, constants.SCREEN_TITLE, fullscreen=constants.FULLSCREEN)

        self.modes = ["оконный", "полный экран"]
        self.mode_idx = 0

        self.raz = [(800, 600), (1280, 720), (1366, 768), (1600, 900), (1920, 1080)]
        self.raz_sey = 0

        self.fov = [1.0, 0.75, 0.5, 0.25]
        self.fov_sey = 0

        self.brightness_labels = ["100%", "75%", "50%", "25%"]
        self.brightness_values = [1.0, 0.75, 0.5, 0.25]
        self.brightness_idx = 0

        self._btn_settings_back = None
        self.game_over_flag = False
        self.paused = False
        self.nastroiki = False
        self.need_restart = False
        self._btn_resume = None
        self._btn_settings = None
        self._btn_exit = None

        self.player_speed_normal = 180.0
        self.player_speed_shift = 260.0

        self.e_key_pressed = False
        self.e_key_press_time = 0.0

    def setup(self):
        self.camera = camera()

        self.ui_scale = min(self.width / constants.SCREEN_WIDTH, self.height / constants.SCREEN_HEIGHT)
        self.camera.world_camera.zoom = self.ui_scale
        self.camera.gui_camera.zoom = 1.0

        self.psycho = Psycho(self.camera, x=constants.SCREEN_WIDTH // 2, y=constants.SCREEN_HEIGHT // 2)
        self.psycho.current_speed = self.player_speed_normal
        self.psycho_list = arcade.SpriteList()
        self.psycho_list.append(self.psycho)

        self.rooms = [Room1(), Room2(), Final()]
        self.Which_room_now = self.rooms[0]

        # Обновляем финальную комнату с учетом текущего разрешения
        self.rooms[2].update_final_image(self.width, self.height)

        self.guard = Guard()
        self.guard.center_x = 1000
        self.guard.center_y = 1000

        self.guard.patrol_points = [(456, 493), (455, 330), (265, 345), (267, 490)]

        base_view_distance = 280
        self.guard.view_distance = base_view_distance * getattr(constants, "VISION_MULTIPLIER", 1.0)
        self.guard.view_angle = 65

        self.guards_list = arcade.SpriteList()
        self.guards_list.append(self.guard)

        self.physics_engine = arcade.PhysicsEngineSimple(self.psycho, self.Which_room_now.walls)

        self.debug_vision = True
        self.game_over_flag = False
        self.base_view_distance = 250

    def on_draw(self):
        if isinstance(self.Which_room_now, Final):
            self.clear()
            self.camera.world_camera.use()
            self.Which_room_now.all_textures_room.draw()

            # В финальной комнате тоже доступны настройки
            if self.paused and not self.game_over_flag and not self.nastroiki:
                self._draw_pause_menu()
            elif self.nastroiki:
                self._draw_settings_menu()

            self.camera.gui_camera.use()
            return

        self.clear()

        self.camera.camera_shake.update_camera()
        self.camera.world_camera.use()

        self.Which_room_now.all_textures_room.draw()
        self.psycho_list.draw()

        if isinstance(self.Which_room_now, Room2):
            self.guards_list.draw()
            self.Which_room_now.phone.draw_hint(self.psycho)
            self.Which_room_now.door2.draw_hint(self.psycho)

        if self.debug_vision and not self.game_over_flag:
            self.guard.draw_vision_cone()

        self.camera.camera_shake.readjust_camera()

        self.camera.gui_camera.position = (self.width // 2, self.height // 2)
        self.camera.gui_camera.use()

        if self.game_over_flag:
            arcade.draw_lrbt_rectangle_filled(0, self.width, 0, self.height, (0, 0, 0, 180))
            arcade.draw_text(
                "ТЫ ПОМЕР!",
                self.width // 2, self.height // 2,
                arcade.color.RED, 72, bold=True,
                anchor_x="center", anchor_y="center"
            )
            arcade.draw_text(
                "Нажмите ESC для выхода",
                self.width // 2, self.height // 2 - 80,
                arcade.color.WHITE, 24,
                anchor_x="center", anchor_y="center"
            )

        if self.paused and not self.game_over_flag and not self.nastroiki:
            self._draw_pause_menu()

        if self.nastroiki:
            self._draw_settings_menu()

        if getattr(constants, "BRIGHTNESS", 1.0) < 1.0:
            alpha = int((1.0 - constants.BRIGHTNESS) * 255)
            arcade.draw_lrbt_rectangle_filled(0, self.width, 0, self.height, (0, 0, 0, alpha))

    def _draw_pause_menu(self):
        arcade.draw_lrbt_rectangle_filled(0, self.width, 0, self.height, (0, 0, 0, 160))

        cx = self.width // 2
        cy = self.height // 2

        arcade.draw_rect_filled(
            arcade.rect.XYWH(cx, cy, 400, 400),
            (23, 26, 33)
        )

        arcade.draw_text("ПАУЗА", cx, cy + 150, arcade.color.WHITE, 36,
                         anchor_x="center", anchor_y="center", bold=True)

        self._btn_resume = (cx, cy + 75, 260, 60)
        self._btn_settings = (cx, cy, 260, 60)
        self._btn_exit = (cx, cy - 75, 260, 60)

        def draw_btn(btn, text):
            bx, by, bw, bh = btn
            arcade.draw_rect_filled(
                arcade.rect.XYWH(bx, by, bw, bh),
                (255, 185, 35)
            )

            arcade.draw_text(text, bx, by, (34, 26, 37), 25,
                             anchor_x="center", anchor_y="center", bold=True)

        draw_btn(self._btn_resume, "ПРОДОЛЖИТЬ")
        draw_btn(self._btn_settings, "НАСТРОЙКИ")
        draw_btn(self._btn_exit, "ВЫЙТИ")

    def _draw_settings_menu(self):
        cx = self.width // 2
        cy = self.height // 2
        self._recalc_settings_hit()

        arcade.draw_rect_filled(
            arcade.rect.XYWH(cx, cy + 50, 800, 500),
            arcade.color.LIGHT_GRAY
        )

        arcade.draw_text(
            "НАСТРОЙКИ",
            cx, cy + 250,
            arcade.color.BLACK,
            font_size=36,
            anchor_x="center", anchor_y="center",
            bold=True
        )

        label_x = cx - 268
        value_x = cx + 82
        x1 = cx - 88
        x2 = cx + 272

        y3 = cy + 170
        arcade.draw_text("РАЗМЕР ЭКРАНА", label_x, y3, arcade.color.BLACK, 28,
                         anchor_x="center", anchor_y="center", bold=True)

        arcade.draw_text(f"{self.modes[self.mode_idx]}", value_x, y3, arcade.color.BLACK, 28,
                         anchor_x="center", anchor_y="center", bold=True)

        arcade.draw_triangle_filled(x1 + 15, y3 + 20, x1 + 15, y3 - 20, x1 - 15, y3, arcade.color.GREEN)
        arcade.draw_triangle_filled(x2 - 15, y3 + 20, x2 - 15, y3 - 20, x2 + 15, y3, arcade.color.GREEN)

        y1 = cy + 110
        arcade.draw_text("РАЗРЕШЕНИЕ", label_x, y1, arcade.color.BLACK, 28,
                         anchor_x="center", anchor_y="center", bold=True)

        arcade.draw_triangle_filled(x1 + 15, y1 + 20, x1 + 15, y1 - 20, x1 - 15, y1, arcade.color.GREEN)
        arcade.draw_triangle_filled(x2 - 15, y1 + 20, x2 - 15, y1 - 20, x2 + 15, y1, arcade.color.GREEN)

        if self.mode_idx == 1:
            arcade.draw_text("НЕДОСТУПНО", value_x, y1, arcade.color.BLACK, 28,
                             anchor_x="center", anchor_y="center", bold=True)
        else:
            arcade.draw_text(f"{self.raz[self.raz_sey][0]}x{self.raz[self.raz_sey][1]}",
                             value_x, y1, arcade.color.BLACK, 28,
                             anchor_x="center", anchor_y="center", bold=True)

        y4 = cy + 50
        arcade.draw_text("FOV охранника", label_x, y4, arcade.color.BLACK, 28,
                         anchor_x="center", anchor_y="center", bold=True)

        arcade.draw_triangle_filled(x1 + 15, y4 + 20, x1 + 15, y4 - 20, x1 - 15, y4, arcade.color.GREEN)
        arcade.draw_triangle_filled(x2 - 15, y4 + 20, x2 - 15, y4 - 20, x2 + 15, y4, arcade.color.GREEN)

        arcade.draw_text(f"{self.fov[self.fov_sey]}", value_x, y4, arcade.color.BLACK, 28,
                         anchor_x="center", anchor_y="center", bold=True)

        y5 = cy - 10
        arcade.draw_text("Яркость", label_x, y5, arcade.color.BLACK, 28,
                         anchor_x="center", anchor_y="center", bold=True)

        arcade.draw_triangle_filled(x1 + 15, y5 + 20, x1 + 15, y5 - 20, x1 - 15, y5, arcade.color.GREEN)
        arcade.draw_triangle_filled(x2 - 15, y5 + 20, x2 - 15, y5 - 20, x2 + 15, y5, arcade.color.GREEN)

        arcade.draw_text(f"{self.brightness_labels[self.brightness_idx]}", value_x, y5, arcade.color.BLACK, 28,
                         anchor_x="center", anchor_y="center", bold=True)

        btn_y = cy - 160
        self._btn_settings_back = (cx, btn_y, 260, 60)

        arcade.draw_rect_filled(
            arcade.rect.XYWH(cx, btn_y, 260, 60),
            (255, 185, 35)
        )
        arcade.draw_text(
            "НАЗАД",
            cx, btn_y,
            (34, 26, 37),
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        if self.need_restart:
            arcade.draw_text(
                "Для применения нужно перезапустить игру",
                cx, cy - 215,
                arcade.color.RED,
                font_size=18,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

    def _recalc_settings_hit(self):
        cx = self.width // 2
        cy = self.height // 2

        x1 = cx - 88
        x2 = cx + 272

        y3 = cy + 170
        y1 = cy + 110
        y4 = cy + 50
        y5 = cy - 10

        self._settings_hit = {
            "mode": {"left": (x1, y3), "right": (x2, y3)},
            "res": {"left": (x1, y1), "right": (x2, y1)},
            "fov": {"left": (x1, y4), "right": (x2, y4)},
            "brightness": {"left": (x1, y5), "right": (x2, y5)},
        }

    def on_update(self, delta_time):
        if self.game_over_flag or (self.paused and not isinstance(self.Which_room_now, Final)) or self.nastroiki:
            return

        if isinstance(self.Which_room_now, Room2):
            self.Which_room_now.phone.update(delta_time)

        if isinstance(self.Which_room_now, Room2):
            door2 = self.Which_room_now.door2
            if door2.is_player_near(self.psycho) and self.e_key_pressed:
                if not door2.is_interacting:
                    door2.start_interaction()

                success = door2.update_interaction(delta_time, self.psycho, self.guard)

                if success:
                    self.Which_room_now = self.rooms[2]

                    self.psycho.center_x = constants.SCREEN_WIDTH // 2
                    self.psycho.center_y = constants.SCREEN_HEIGHT // 2

                    self.physics_engine = arcade.PhysicsEngineSimple(
                        self.psycho,
                        arcade.SpriteList()
                    )
            else:
                if door2.is_interacting:
                    door2.cancel_interaction()

        if not isinstance(self.Which_room_now, Final):
            if arcade.check_for_collision(self.psycho, self.Which_room_now.door):
                self.Which_room_now = self.rooms[self.Which_room_now.door.next_room]

                self.psycho.center_x = self.Which_room_now.door.spawn_coordinates[0]
                self.psycho.center_y = self.Which_room_now.door.spawn_coordinates[1]

                self.guard.center_x = self.Which_room_now.door.spawn_guard[0]
                self.guard.center_y = self.Which_room_now.door.spawn_guard[1]

                self.physics_engine = arcade.PhysicsEngineSimple(self.psycho, self.Which_room_now.walls)

                self.guard_engine = arcade.PhysicsEngineSimple(self.guard, self.Which_room_now.walls)

        self.physics_engine.update()
        self.psycho.update(delta_time)

        self.camera.camera_shake.update(delta_time)

        if not isinstance(self.Which_room_now, Final):
            self.guard.update(delta_time, self.psycho, self.Which_room_now.walls)

        if isinstance(self.Which_room_now, Final):
            self.camera.world_camera.position = (constants.SCREEN_WIDTH // 2,
            constants.SCREEN_HEIGHT // 2)
        else:
            self.camera.world_camera.position = (self.psycho.center_x, self.psycho.center_y)

        if self.psycho.hp <= 0:
            self.game_over()

    def on_key_press(self, key, modifiers):
        # В финальной комнате тоже можно открывать меню паузы/настроек
        if self.game_over_flag:
            if key == arcade.key.ESCAPE:
                arcade.close_window()
            return

        if key == arcade.key.ESCAPE:
            if self.nastroiki:
                if self.need_restart:
                    arcade.close_window()
                    return
                self.nastroiki = False
            else:
                self.paused = not self.paused
            return

        if key == arcade.key.V and not isinstance(self.Which_room_now, Final):
            self.debug_vision = not self.debug_vision
            return

        if key == arcade.key.E and isinstance(self.Which_room_now, Room2):
            self.e_key_pressed = True

            phone = self.Which_room_now.phone
            if phone.is_player_near(self.psycho) and not phone.activated:
                phone.activate()
                self.guard.move_to_point(267, 490, walls=self.Which_room_now.walls)

        if not isinstance(self.Which_room_now, Final):
            if modifiers & arcade.key.MOD_SHIFT:
                self.psycho.current_speed = self.player_speed_shift
            else:
                self.psycho.current_speed = self.player_speed_normal

            self.psycho.on_key_press(key)

    def on_key_release(self, key, modifiers):
        if self.game_over_flag:
            return

        if key == arcade.key.E and isinstance(self.Which_room_now, Room2):
            self.e_key_pressed = False
            self.Which_room_now.door2.cancel_interaction()

        if not isinstance(self.Which_room_now, Final):
            if not (modifiers & arcade.key.MOD_SHIFT):
                self.psycho.current_speed = self.player_speed_normal

            self.psycho.on_key_release(key)

    def _hit_triangle(self, px, py, tx, ty):
        return (tx - 20 <= px <= tx + 20) and (ty - 25 <= py <= ty + 25)

    def on_mouse_press(self, x, y, button, modifiers):
        # В финальной комнате тоже доступно меню настроек
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if self.nastroiki:
            if not hasattr(self, "_settings_hit"):
                self._recalc_settings_hit()

            h = self._settings_hit

            def hit(btn):
                bx, by, bw, bh = btn
                return (bx - bw / 2 <= x <= bx + bw / 2) and (by - bh / 2 <= y <= by + bh / 2)

            if self._btn_settings_back and hit(self._btn_settings_back):
                if self.need_restart:
                    arcade.close_window()
                    return
                self.nastroiki = False
                return

            if self.mode_idx == 0:
                if self._hit_triangle(x, y, *h["res"]["left"]):
                    self.raz_sey = (self.raz_sey - 1) % len(self.raz)
                    constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT = self.raz[self.raz_sey]
                    self.need_restart = True

                elif self._hit_triangle(x, y, *h["res"]["right"]):
                    self.raz_sey = (self.raz_sey + 1) % len(self.raz)
                    constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT = self.raz[self.raz_sey]
                    self.need_restart = True

            if self._hit_triangle(x, y, *h["mode"]["left"]):
                self.mode_idx = (self.mode_idx - 1) % len(self.modes)
                constants.FULLSCREEN = (self.mode_idx == 1)
                self.need_restart = True

            elif self._hit_triangle(x, y, *h["mode"]["right"]):
                self.mode_idx = (self.mode_idx + 1) % len(self.modes)
                constants.FULLSCREEN = (self.mode_idx == 1)
                self.need_restart = True

            if self._hit_triangle(x, y, *h["fov"]["left"]):
                self.fov_sey = (self.fov_sey + 1) % len(self.fov)
                constants.VISION_MULTIPLIER = self.fov[self.fov_sey]
                if not isinstance(self.Which_room_now, Final):
                    self.guard.view_distance = self.base_view_distance * constants.VISION_MULTIPLIER

            elif self._hit_triangle(x, y, *h["fov"]["right"]):
                self.fov_sey = (self.fov_sey - 1) % len(self.fov)
                constants.VISION_MULTIPLIER = self.fov[self.fov_sey]
                if not isinstance(self.Which_room_now, Final):
                    self.guard.view_distance = self.base_view_distance * constants.VISION_MULTIPLIER

            if self._hit_triangle(x, y, *h["brightness"]["left"]):
                self.brightness_idx = (self.brightness_idx + 1) % len(self.brightness_values)
                constants.BRIGHTNESS = self.brightness_values[self.brightness_idx]

            elif self._hit_triangle(x, y, *h["brightness"]["right"]):
                self.brightness_idx = (self.brightness_idx - 1) % len(self.brightness_values)
                constants.BRIGHTNESS = self.brightness_values[self.brightness_idx]

            return

        if not self.paused or self.game_over_flag:
            return

        def hit(btn):
            bx, by, bw, bh = btn
            return (bx - bw / 2 <= x <= bx + bw / 2) and (by - bh / 2 <= y <= by + bh / 2)

        if self._btn_resume and hit(self._btn_resume):
            self.paused = False

        elif self._btn_exit and hit(self._btn_exit):
            arcade.close_window()

        elif self._btn_settings and hit(self._btn_settings):
            self.nastroiki = True

    def game_over(self):
        self.game_over_flag = True
        self.psycho.change_x = 0
        self.psycho.change_y = 0
        self.guard.change_x = 0
        self.guard.change_y = 0


def main():
    game = The_psycho_escape()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()