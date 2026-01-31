import arcade
import constants

from psycho import Psycho
from room import Room1, Room2
from guard import Guard
from Camera import camera


class The_psycho_escape(arcade.Window):
    def __init__(self):
        w = getattr(constants, "WINDOW_WIDTH", constants.SCREEN_WIDTH)
        h = getattr(constants, "WINDOW_HEIGHT", constants.SCREEN_HEIGHT)

        super().__init__(w, h, constants.SCREEN_TITLE, fullscreen=constants.FULLSCREEN)

        self.game_over_flag = False
        self.paused = False

        self._btn_resume = None
        self._btn_settings = None
        self._btn_exit = None

        self.player_speed_normal = 180.0
        self.player_speed_shift = 260.0

    def setup(self):
        self.camera = camera()

        self.ui_scale = min(self.width / constants.SCREEN_WIDTH, self.height / constants.SCREEN_HEIGHT)
        self.camera.world_camera.zoom = self.ui_scale
        self.camera.gui_camera.zoom = 1.0

        self.psycho = Psycho(self.camera, x=constants.SCREEN_WIDTH // 2, y=constants.SCREEN_HEIGHT // 2)
        self.psycho.current_speed = self.player_speed_normal
        self.psycho_list = arcade.SpriteList()
        self.psycho_list.append(self.psycho)

        self.rooms = [Room1(), Room2()]
        self.Which_room_now = self.rooms[0]

        self.guard = Guard()
        self.guard.center_x = 620
        self.guard.center_y = 500
        self.guard.patrol_points = [
            (680, 495),
            (680, 300),
            (500, 300),
            (500, 495),
        ]

        base_view_distance = 300
        self.guard.view_distance = base_view_distance * getattr(constants, "VISION_MULTIPLIER", 1.0)
        self.guard.view_angle = 90

        self.guards_list = arcade.SpriteList()
        self.guards_list.append(self.guard)

        self.physics_engine = arcade.PhysicsEngineSimple(self.psycho, self.Which_room_now.walls)

        self.debug_vision = True
        self.game_over_flag = False

    def on_draw(self):
        self.clear()

        self.camera.camera_shake.update_camera()
        self.camera.world_camera.use()

        self.Which_room_now.all_textures_room.draw()
        self.psycho_list.draw()
        self.guards_list.draw()

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

        if self.paused and not self.game_over_flag:
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

        if getattr(constants, "BRIGHTNESS", 1.0) < 1.0:
            alpha = int((1.0 - constants.BRIGHTNESS) * 255)
            arcade.draw_lrbt_rectangle_filled(0, self.width, 0, self.height, (0, 0, 0, alpha))

    def on_update(self, delta_time):
        if self.game_over_flag or self.paused:
            return

        if arcade.check_for_collision(self.psycho, self.Which_room_now.door):
            self.Which_room_now = self.rooms[self.Which_room_now.door.next_room]

            self.psycho.center_x = self.Which_room_now.door.spawn_coordinates[0]
            self.psycho.center_y = self.Which_room_now.door.spawn_coordinates[1]

            self.physics_engine = arcade.PhysicsEngineSimple(self.psycho, self.Which_room_now.walls)
            self.guard_engine = arcade.PhysicsEngineSimple(self.guard, self.Which_room_now.walls)

        self.physics_engine.update()
        self.psycho.update(delta_time)

        self.camera.camera_shake.update(delta_time)

        self.guard.update(delta_time, self.psycho, self.Which_room_now.walls)

        self.camera.world_camera.position = (self.psycho.center_x, self.psycho.center_y)

        if self.psycho.hp <= 0:
            self.game_over()

    def on_key_press(self, key, modifiers):
        if self.game_over_flag:
            if key == arcade.key.ESCAPE:
                arcade.close_window()
            return

        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
            return

        if key == arcade.key.V:
            self.debug_vision = not self.debug_vision
            return

        if modifiers & arcade.key.MOD_SHIFT:
            self.psycho.current_speed = self.player_speed_shift
        else:
            self.psycho.current_speed = self.player_speed_normal

        self.psycho.on_key_press(key)

    def on_key_release(self, key, modifiers):
        if self.game_over_flag:
            return

        if not (modifiers & arcade.key.MOD_SHIFT):
            self.psycho.current_speed = self.player_speed_normal

        self.psycho.on_key_release(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
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
            print("НАСТРОЙКИ (пока заглушка)")

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
