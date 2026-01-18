import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from player import Psycho
from room import Room
from wall import Wall
from guard import Guard


class The_psycho_escape(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game_over_flag = False

    def setup(self):
        self.psycho = Psycho()
        self.psycho_list = arcade.SpriteList()
        self.psycho_list.append(self.psycho)

        self.walls = arcade.SpriteList()
        wall = Wall()
        self.walls.append(wall)

        self.room = Room()
        self.room_list = arcade.SpriteList()
        self.room_list.append(self.room)

        self.guard = Guard()
        self.guard.center_x = 100
        self.guard.center_y = 100
        self.guard.patrol_points = [
            (100, 100),
            (400, 100),
            (400, 400),
            (100, 400)
        ]
        self.guards_list = arcade.SpriteList()
        self.guards_list.append(self.guard)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.psycho,
            self.walls
        )

        self.guard_physics_engine = arcade.PhysicsEngineSimple(
            self.guard,
            self.walls
        )

        self.debug_vision = True
        self.game_over_flag = False

    def on_draw(self):
        self.clear()

        self.room_list.draw()
        self.walls.draw()
        self.psycho_list.draw()
        self.guards_list.draw()

        if self.debug_vision and not self.game_over_flag:
            self.guard.draw_vision_cone()

        if self.game_over_flag:
            arcade.draw_lrbt_rectangle_filled(left=0, right=SCREEN_WIDTH, bottom=0, top=SCREEN_HEIGHT,
                                              color=(0, 0, 0, 180))

            arcade.draw_text("ВЫ ПРОИГРАЛИ!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.RED, 72, bold=True,
                             anchor_x="center", anchor_y="center")

            arcade.draw_text("Нажмите ESC для выхода", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80, arcade.color.WHITE,
                             24, anchor_x="center", anchor_y="center")

    def on_update(self, delta_time):
        if self.game_over_flag:
            return

        self.physics_engine.update()
        self.psycho.update(delta_time)

        self.guard_physics_engine.update()
        self.guard.update(delta_time, self.psycho, self.walls)

        if self.psycho.hp <= 0:
            self.game_over()

    def on_key_press(self, key, modifiers):
        if self.game_over_flag:
            if key == arcade.key.ESCAPE:
                arcade.close_window()
            return

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

        if key == arcade.key.V:
            self.debug_vision = not self.debug_vision


    def on_key_release(self, key, modifiers):
        if self.game_over_flag:
            return

        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.psycho.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.psycho.change_x = 0

        if not (modifiers & arcade.key.MOD_SHIFT):
            self.psycho.current_speed = self.psycho.normal_speed

    def game_over(self):
        self.game_over_flag = True
        self.psycho.change_x = 0
        self.psycho.change_y = 0
        self.guard.change_x = 0
        self.guard.change_y = 0


def main():
    game = The_psycho_escape(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
