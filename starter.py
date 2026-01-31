import main
import arcade
import constants

SCREEN_WIDTH = 1376
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Фабрика иллюзий"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.w = width
        self.h = height
        self.nastoiki = False
        self.texture = arcade.load_texture(r"images\start.jpg")
        self.raz = [
            (800, 600),
            (1280, 720),
            (1600, 900),
            (1920, 1080),
            (2560, 1440)
        ]
        self.raz_sey = 1
        self.modes = ["ОКОННЫЙ", "ПОЛНОЭКРАННЫЙ"]
        self.mode_idx = 0
        self.fov = ['100%', '75%', '50%', '25%']
        self.fov_values = [1.0, 0.75, 0.5, 0.25]
        self.fov_sey = 0
        self.brightness_labels = ['100%', '75%', '50%', '25%']
        self.brightness_values = [1.0, 0.75, 0.5, 0.25]
        self.brightness_idx = 0

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(1376 // 2, 768 // 2, self.w, self.h))
        arcade.draw_rect_filled(arcade.rect.XYWH(500, 100, 300, 100), arcade.color.WHITE)
        arcade.draw_text("ИГРАТЬ", 500, 100, arcade.color.BLACK, font_size=36, anchor_x="center",
                         anchor_y="center", bold=True)
        arcade.draw_rect_filled(arcade.rect.XYWH(850, 100, 300, 100), arcade.color.WHITE)
        arcade.draw_text("НАСТРОЙКИ", 850, 100, arcade.color.BLACK, font_size=36, anchor_x="center",
                         anchor_y="center", bold=True)
        if self.nastoiki:
            arcade.draw_rect_filled(arcade.rect.XYWH(1376 // 2, 768 // 2 + 50, 800, 500), arcade.color.LIGHT_GRAY)
            arcade.draw_text("НАСТРОЙКИ", 688, 640, arcade.color.BLACK, font_size=36, anchor_x="center",
                             anchor_y="center", bold=True)
            arcade.draw_text("РАЗМЕР ЭКРАНА", 420, 560, arcade.color.BLACK, font_size=28, anchor_x="center",
                             anchor_y="center", bold=True)
            arcade.draw_text(f'{self.modes[self.mode_idx]}', 770, 560, arcade.color.BLACK,
                             font_size=28,
                             anchor_x="center",
                             anchor_y="center", bold=True)
            x1 = 600
            y3 = 560
            arcade.draw_triangle_filled(x1 + 15, y3 + 20, x1 + 15, y3 - 20, x1 - 15, y3, arcade.color.GREEN)
            x2 = 960
            arcade.draw_triangle_filled(x2 - 15, y3 + 20, x2 - 15, y3 - 20, x2 + 15, y3, arcade.color.GREEN)

            arcade.draw_text("РАЗРЕШЕНИЕ", 420, 500, arcade.color.BLACK, font_size=28, anchor_x="center",
                             anchor_y="center", bold=True)
            y1 = 495
            arcade.draw_triangle_filled(x1 + 15, y1 + 20, x1 + 15, y1 - 20, x1 - 15, y1, arcade.color.GREEN)
            arcade.draw_triangle_filled(x2 - 15, y1 + 20, x2 - 15, y1 - 20, x2 + 15, y1, arcade.color.GREEN)
            if self.mode_idx == 1:
                arcade.draw_text(f'НЕДОСТУПНО', 770, 500, arcade.color.BLACK, font_size=28,
                                 anchor_x="center", anchor_y="center", bold=True)
            else:
                arcade.draw_text(f'{self.raz[self.raz_sey][0]}x{self.raz[self.raz_sey][1]}', 770, 500,
                                 arcade.color.BLACK, font_size=28, anchor_x="center", anchor_y="center", bold=True)

            y4 = 440
            arcade.draw_text("FOV охранника", 420, 440, arcade.color.BLACK, font_size=28, anchor_x="center",
                             anchor_y="center", bold=True)
            arcade.draw_triangle_filled(x1 + 15, y4 + 20, x1 + 15, y4 - 20, x1 - 15, y4, arcade.color.GREEN)
            arcade.draw_triangle_filled(x2 - 15, y4 + 20, x2 - 15, y4 - 20, x2 + 15, y4, arcade.color.GREEN)
            arcade.draw_text(f'{self.fov[self.fov_sey]}', 770, y4, arcade.color.BLACK,
                             font_size=28,
                             anchor_x="center",
                             anchor_y="center", bold=True)
            y5 = 380
            arcade.draw_text("Яркость", 420, y5, arcade.color.BLACK, font_size=28, anchor_x="center",
                             anchor_y="center", bold=True)
            arcade.draw_triangle_filled(x1 + 15, y5 + 20, x1 + 15, y5 - 20, x1 - 15, y5, arcade.color.GREEN)
            arcade.draw_triangle_filled(x2 - 15, y5 + 20, x2 - 15, y5 - 20, x2 + 15, y5, arcade.color.GREEN)
            arcade.draw_text(f'{self.brightness_labels[self.brightness_idx]}', 770, y5, arcade.color.BLACK,
                             font_size=28,
                             anchor_x="center",
                             anchor_y="center", bold=True)

    def on_mouse_press(self, x, y, button, modifiers):
        x1 = 600
        y1 = 495
        x2 = 960
        y3 = 560
        y4 = 440
        y5 = 380
        if button == arcade.MOUSE_BUTTON_LEFT:
            if 350 <= x <= 650 and 50 <= y <= 150:
                constants.FULLSCREEN = (self.mode_idx == 1)
                arcade.close_window()
                constants.VISION_MULTIPLIER = self.fov_values[self.fov_sey]
                constants.BRIGHTNESS = self.brightness_values[self.brightness_idx]

                if not constants.FULLSCREEN:
                    constants.WINDOW_WIDTH = self.raz[self.raz_sey][0]
                    constants.WINDOW_HEIGHT = self.raz[self.raz_sey][1]

                main.main()
            if 700 <= x <= 1000 and 50 <= y <= 150:
                self.nastoiki = not self.nastoiki
            if self.nastoiki:
                if (x1 - 15 <= x <= x1 + 15) and (y1 - 20 <= y <= y1 + 20):
                    self.raz_sey = (self.raz_sey - 1) % len(self.raz)
                if (x2 - 15 <= x <= x2 + 15) and (y1 - 20 <= y <= y1 + 20):
                    self.raz_sey = (self.raz_sey + 1) % len(self.raz)

                if (x1 - 15 <= x <= x1 + 15) and (y3 - 20 <= y <= y3 + 20):
                    self.mode_idx = (self.mode_idx - 1) % len(self.modes)
                if (x2 - 15 <= x <= x2 + 15) and (y3 - 20 <= y <= y3 + 20):
                    self.mode_idx = (self.mode_idx + 1) % len(self.modes)

                if (x1 - 15 <= x <= x1 + 15) and (y4 - 20 <= y <= y4 + 20):
                    self.fov_sey = (self.fov_sey + 1) % len(self.fov)
                if (x2 - 15 <= x <= x2 + 15) and (y4 - 20 <= y <= y4 + 20):
                    self.fov_sey = (self.fov_sey - 1) % len(self.fov)

                if (x1 - 15 <= x <= x1 + 15) and (y5 - 20 <= y <= y5 + 20):
                    self.brightness_idx = (self.brightness_idx + 1) % len(self.brightness_labels)
                if (x2 - 15 <= x <= x2 + 15) and (y5 - 20 <= y <= y5 + 20):
                    self.brightness_idx = (self.brightness_idx - 1) % len(self.brightness_labels)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.nastoiki = not self.nastoiki


def main1():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main1()
