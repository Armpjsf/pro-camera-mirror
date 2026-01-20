from kivy.app import App  # type: ignore
from kivy.uix.floatlayout import FloatLayout  # type: ignore
from kivy.uix.scatterlayout import ScatterLayout  # type: ignore
from kivy.uix.camera import Camera  # type: ignore
from kivy.uix.button import Button  # type: ignore
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
        self.camera_wrapper = ScatterLayout(
            do_translation=False, do_rotation=False, do_scale=False
        )

        # 3. เรียกใช้กล้องหลัง (index=0) - แก้ไข keep_ratio = True เพื่อไม่ให้ภาพบีบ
        self.camera = Camera(play=True, index=0, resolution=(1920, 1080))
        self.camera.allow_stretch = True
        self.camera.keep_ratio = True  # แก้ไขเป็น True เพื่อรักษา aspect ratio

        # ใส่กล้องเข้าไปใน Wrapper
        self.camera_wrapper.add_widget(self.camera)
        self.root.add_widget(self.camera_wrapper)

        # 4. เลเยอร์ปรับความสว่าง (Brightness Overlay)
        self.brightness_level = 0.0
        self.exposure_compensation = 0  # ค่า exposure เริ่มต้น
        with self.root.canvas.after:
            Color(1, 1, 1, self.brightness_level, mode="add")
            self.bright_rect = Rectangle(pos=self.root.pos, size=Window.size)

        # Event Bindings
        self.root.bind(size=self._update_rect, pos=self._update_rect)

        # ค่าเริ่มต้น: กลับด้านแนวนอนทันที (Mirror)
        self.camera_wrapper.scale_x = -1

        # 5. สร้างเมนูควบคุม (Auto-hiding Menu)
        self.menu_visible = False
        self.hide_timer = None
        self.create_control_menu()
        self.hide_menu()  # เริ่มต้นซ่อนเมนู

        # Bind window resize to update button positions
        Window.bind(size=self._update_button_positions)

        return self.root

    def create_control_menu(self):
        """สร้างเมนูปุ่มควบคุม"""
        self.button_height = 60
        button_width = 180
        spacing = 10
        x_pos = 10

        # ปุ่มกลับด้านกระจก
        self.btn_mirror = Button(
            text="🔄 Mirror",
            size_hint=(None, None),
            size=(button_width, self.button_height),
            pos=(x_pos, Window.height - self.button_height - spacing),
            background_color=(0.2, 0.6, 0.8, 0.9),
            font_size=18,
        )
        self.btn_mirror.bind(on_press=self.toggle_mirror)
        self.root.add_widget(self.btn_mirror)

        # ปุ่มเพิ่มความสว่าง Overlay
        self.btn_brightness_up = Button(
            text="☀️ +Bright",
            size_hint=(None, None),
            size=(button_width, self.button_height),
            pos=(x_pos, Window.height - 2 * (self.button_height + spacing)),
            background_color=(0.9, 0.7, 0.2, 0.9),
            font_size=18,
        )
        self.btn_brightness_up.bind(on_press=self.increase_brightness)
        self.root.add_widget(self.btn_brightness_up)

        # ปุ่มลดความสว่าง Overlay
        self.btn_brightness_down = Button(
            text="🌙 -Bright",
            size_hint=(None, None),
            size=(button_width, self.button_height),
            pos=(x_pos, Window.height - 3 * (self.button_height + spacing)),
            background_color=(0.5, 0.5, 0.5, 0.9),
            font_size=18,
        )
        self.btn_brightness_down.bind(on_press=self.decrease_brightness)
        self.root.add_widget(self.btn_brightness_down)

        # ปุ่มเพิ่ม Exposure (กล้องสว่างขึ้น)
        self.btn_exposure_up = Button(
            text="📷+ Exposure",
            size_hint=(None, None),
            size=(button_width, self.button_height),
            pos=(x_pos, Window.height - 4 * (self.button_height + spacing)),
            background_color=(0.2, 0.8, 0.4, 0.9),
            font_size=18,
        )
        self.btn_exposure_up.bind(on_press=self.increase_exposure)
        self.root.add_widget(self.btn_exposure_up)

        # ปุ่มลด Exposure (กล้องมืดลง)
        self.btn_exposure_down = Button(
            text="📷- Exposure",
            size_hint=(None, None),
            size=(button_width, self.button_height),
            pos=(x_pos, Window.height - 5 * (self.button_height + spacing)),
            background_color=(0.8, 0.3, 0.3, 0.9),
            font_size=18,
        )
        self.btn_exposure_down.bind(on_press=self.decrease_exposure)
        self.root.add_widget(self.btn_exposure_down)

        # เก็บปุ่มทั้งหมดไว้ใน list
        self.menu_buttons = [
            self.btn_mirror,
            self.btn_brightness_up,
            self.btn_brightness_down,
            self.btn_exposure_up,
            self.btn_exposure_down,
        ]

    def show_menu(self):
        """แสดงเมนู"""
        for btn in self.menu_buttons:
            btn.opacity = 1
            btn.disabled = False
        self.menu_visible = True

        # ตั้งเวลาซ่อนเมนูอัตโนมัติหลัง 3 วินาที
        if self.hide_timer:
            self.hide_timer.cancel()
        self.hide_timer = Clock.schedule_once(lambda dt: self.hide_menu(), 3)

    def hide_menu(self):
        """ซ่อนเมนู"""
        for btn in self.menu_buttons:
            btn.opacity = 0
            btn.disabled = True
        self.menu_visible = False

    def toggle_mirror(self, instance):
        """กลับด้านกระจก"""
        self.camera_wrapper.scale_x *= -1
        self.show_menu()  # รีเซ็ตเวลาซ่อนเมนู

    def increase_brightness(self, instance):
        """เพิ่มความสว่าง Overlay"""
        self.brightness_level = min(self.brightness_level + 0.1, 1.0)
        self.update_brightness_overlay()
        self.show_menu()

    def decrease_brightness(self, instance):
        """ลดความสว่าง Overlay"""
        self.brightness_level = max(self.brightness_level - 0.1, 0.0)
        self.update_brightness_overlay()
        self.show_menu()

    def increase_exposure(self, instance):
        """เพิ่ม Exposure (ทำให้กล้องสว่างขึ้น)"""
        self.exposure_compensation = min(self.exposure_compensation + 1, 6)
        self.apply_camera_settings()
        self.show_menu()

    def decrease_exposure(self, instance):
        """ลด Exposure (ทำให้กล้องมืดลง)"""
        self.exposure_compensation = max(self.exposure_compensation - 1, -6)
        self.apply_camera_settings()
        self.show_menu()

    def apply_camera_settings(self):
        """ปรับค่ากล้อง (exposure compensation)"""
        # หมายเหตุ: Kivy Camera widget ไม่รองรับการปรับ exposure โดยตรง
        # แต่เราสามารถใช้ brightness overlay แทนได้
        # หรือถ้าต้องการควบคุม camera จริงๆ ต้องใช้ jnius เข้าถึง Android Camera API

        # ใช้ brightness overlay เป็นการชดเชยแทน exposure
        self.brightness_level = self.exposure_compensation * 0.05
        self.brightness_level = max(-0.3, min(0.5, self.brightness_level))
        self.update_brightness_overlay()

    def update_brightness_overlay(self):
        """อัปเดตเลเยอร์ความสว่าง"""
        self.root.canvas.after.clear()
        with self.root.canvas.after:
            if self.brightness_level >= 0:
                # เพิ่มแสง (สีขาว)
                Color(1, 1, 1, self.brightness_level, mode="add")
            else:
                # ลดแสง (สีดำ)
                Color(0, 0, 0, abs(self.brightness_level), mode="normal")
            self.bright_rect = Rectangle(pos=self.root.pos, size=self.root.size)

    def _update_rect(self, instance, value):
        """อัปเดตขนาดเมื่อหมุนจอ"""
        self.bright_rect.pos = instance.pos
        self.bright_rect.size = instance.size
        self.camera_wrapper.center = instance.center

    def _update_button_positions(self, instance, value):
        """อัปเดตตำแหน่งปุ่มเมื่อหน้าจอเปลี่ยนขนาด"""
        if not hasattr(self, "menu_buttons"):
            return

        spacing = 10
        x_pos = 10

        for i, btn in enumerate(self.menu_buttons):
            btn.pos = (x_pos, Window.height - (i + 1) * (self.button_height + spacing))

    def on_touch_down(self, touch):
        """แตะหน้าจอเพื่อแสดง/ซ่อนเมนู"""
        # ตรวจสอบว่าแตะที่ปุ่มหรือไม่
        for btn in self.menu_buttons:
            if btn.collide_point(*touch.pos) and not btn.disabled:
                # ให้ปุ่มจัดการ touch event
                return self.root.on_touch_down(touch)

        # ถ้าไม่ได้แตะปุ่ม ให้แสดง/ซ่อนเมนู
        if self.menu_visible:
            self.hide_menu()
        else:
            self.show_menu()
        return True


if __name__ == "__main__":
    ProCameraApp().run()
