import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class camera:
    def __init__(self):
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=0.0,
            acceleration_duration=0.1,
            falloff_time=0.8,
            shake_frequency=12.0,
        )


        self.gui_camera.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self, delta_time):
        self.camera_shake.update(delta_time)
