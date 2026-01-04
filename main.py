from kivy.app import App  # type: ignore
from kivy.uix.floatlayout import FloatLayout  # type: ignore
from kivy.uix.scatterlayout import ScatterLayout  # type: ignore
from kivy.uix.camera import Camera  # type: ignore
from kivy.core.window import Window  # type: ignore
from kivy.graphics import Color, Rectangle  # type: ignore
from kivy.clock import Clock  # type: ignore


class ProCameraApp(App):
    def build(self):
        # 1. ตั้งค่า Full Screen (ซ่อนปุ่ม Android)
        Window.fullscreen = "auto"

        # Main Layout
        self.root = FloatLayout()

        # 2. สร้าง Wrapper สำหรับกลับด้านภาพ (ScatterLayout)
        # เราจะใช้ตัวนี้หมุน/กลับด้านกล้อง
        self.camera_wrapper = ScatterLayout(
            do_translation=False, do_rotation=False, do_scale=False
        )

        # 3. เรียกใช้กล้องหลัง (index=0)
        self.camera = Camera(play=True, index=0, resolution=(1920, 1080))
        self.camera.allow_stretch = True
        self.camera.keep_ratio = False

        # ใส่กล้องเข้าไปใน Wrapper
        self.camera_wrapper.add_widget(self.camera)
        self.root.add_widget(self.camera_wrapper)

        # 4. เลเยอร์ปรับความสว่าง (Brightness Overlay)
        self.brightness_level = 0.0
        with self.root.canvas.after:
            Color(1, 1, 1, self.brightness_level, mode="add")
            self.bright_rect = Rectangle(pos=self.root.pos, size=Window.size)

        # Event Bindings
        self.root.bind(size=self._update_rect, pos=self._update_rect)

        # ค่าเริ่มต้น: กลับด้านแนวนอนทันที (Mirror) เพื่อแก้ปัญหาจอชนทีวี
        # scale_x = -1 คือการกลับซ้ายขวา
        self.camera_wrapper.scale_x = -1

        return self.root

    def _update_rect(self, instance, value):
        # อัปเดตขนาดสี่เหลี่ยมแสงเมื่อหมุนจอ
        self.bright_rect.pos = instance.pos
        self.bright_rect.size = instance.size
        # บังคับให้จุดหมุนอยู่ตรงกลางเสมอ เพื่อให้กลับด้านแล้วภาพไม่เบี้ยว
        self.camera_wrapper.center = instance.center

    def on_touch_down(self, touch):
        # ฟีเจอร์สั่งงานด้วยการแตะ (Gestures)

        if touch.is_double_tap:
            # === แตะ 2 ครั้ง: สลับโหมดกระจก (Flip ซ้าย/ขวา) ===
            # ถ้าเป็น -1 ให้เปลี่ยนเป็น 1, ถ้าเป็น 1 ให้เปลี่ยนเป็น -1
            self.camera_wrapper.scale_x *= -1
            return True

        else:
            # === แตะ 1 ครั้ง: ปรับความสว่าง ===
            self.brightness_level += 0.1
            if self.brightness_level > 0.5:  # ถ้าสว่างเกินไป ให้รีเซ็ต
                self.brightness_level = 0.0

            # วาดเลเยอร์แสงใหม่
            self.root.canvas.after.clear()
            with self.root.canvas.after:
                Color(1, 1, 1, self.brightness_level, mode="add")
                self.bright_rect = Rectangle(pos=self.root.pos, size=self.root.size)

            return True


if __name__ == "__main__":
    ProCameraApp().run()
