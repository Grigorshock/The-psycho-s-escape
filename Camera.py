import arcade
import constants


class camera:
    def __init__(self):
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=10.0,
            acceleration_duration=0.1,
            falloff_time=0.8,
            shake_frequency=12.0,
        )

    def hit_shake(self):
        if hasattr(self.camera_shake, "shake"):
            self.camera_shake.shake()
    def update(self, delta_time: float):
        self.camera_shake.update(delta_time)
