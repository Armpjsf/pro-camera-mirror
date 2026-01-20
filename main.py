from kivy.app import App  # type: ignore
from kivy.uix.floatlayout import FloatLayout  # type: ignore
from kivy.uix.camera import Camera  # type: ignore
from kivy.core.window import Window  # type: ignore
from kivy.graphics import Color, Rectangle  # type: ignore


class ProCameraApp(App):
    def build(self):
        # ตั้งค่า Full Screen
        Window.fullscreen = "auto"

        # Main Layout
        self.root = FloatLayout()

        # สร้างกล้องหลัง
        self.camera = Camera(
            play=True,
            index=0,
            resolution=(1920, 1080),
            allow_stretch=True,
            keep_ratio=True,
        )

        # กลับด้านภาพให้เป็นโหมดกระจกทันที
        self.camera.scale_x = -1
        self.root.add_widget(self.camera)

        # เพิ่มเลเยอร์ความสว่าง (เริ่มต้นที่ 20% เพื่อให้สว่างขึ้น)
        self.brightness_level = 0.2
        with self.root.canvas.after:
            Color(1, 1, 1, self.brightness_level, mode="add")
            self.bright_rect = Rectangle(pos=self.root.pos, size=Window.size)

        # Event binding
        self.root.bind(size=self._update_rect, pos=self._update_rect)
        Window.bind(size=self._update_camera_center)

        return self.root

    def _update_rect(self, instance, value):
        """อัปเดตขนาดเลเยอร์ความสว่าง"""
        self.bright_rect.pos = instance.pos
        self.bright_rect.size = instance.size

    def _update_camera_center(self, instance, value):
        """อัปเดตตำแหน่งกล้องให้อยู่กลางจอ"""
        self.camera.center = self.root.center

    def on_touch_down(self, touch):
        """แตะเพื่อปรับความสว่าง"""
        if touch.is_double_tap:
            # แตะ 2 ครั้ง: กลับด้านกระจก
            self.camera.scale_x *= -1
        else:
            # แตะ 1 ครั้ง: ปรับความสว่างทีละ 15%
            self.brightness_level += 0.15
            if self.brightness_level > 0.8:  # สว่างสุด 80%
                self.brightness_level = 0.0  # รีเซ็ตเป็น 0

            # วาดเลเยอร์แสงใหม่
            self.root.canvas.after.clear()
            with self.root.canvas.after:
                Color(1, 1, 1, self.brightness_level, mode="add")
                self.bright_rect = Rectangle(pos=self.root.pos, size=self.root.size)

        return True


if __name__ == "__main__":
    ProCameraApp().run()
