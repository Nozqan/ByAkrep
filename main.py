import socket, threading, uuid
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse

Window.softinput_mode = "below_target"

class AkrepVipGold(App):
    def build(self):
        self.my_id = str(uuid.getnode())
        self.root = BoxLayout(orientation='vertical')
        
        with self.root.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.bg = Rectangle(pos=self.root.pos, size=self.root.size)
            Color(0.9, 0.1, 0.2, 0.15)
            for i in range(12):
                Ellipse(pos=(50 + i*110, 200 + i*170), size=(110, 110))
        self.root.bind(pos=self.update_rect, size=self.update_rect)

        self.root.add_widget(Label(
            text="[b][color=D4AF37]ByAkrep sizi koruyor[/color][/b]",
            markup=True, size_hint_y=None, height=130, font_size='26sp'
        ))

        self.scroll = ScrollView(size_hint=(1, 1))
        self.chat_logs = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=[15, 20])
        self.chat_logs.bind(minimum_height=self.chat_logs.setter('height'))
        self.scroll.add_widget(self.chat_logs)
        self.root.add_widget(self.scroll)

        input_area = BoxLayout(size_hint_y=None, height=140, padding=12, spacing=10)
        self.input = TextInput(
            hint_text="Bir mesaj yaz...", multiline=False,
            background_color=(0.12, 0.12, 0.12, 1), foreground_color=(1, 1, 1, 1),
            padding=[20, 15], font_size='18sp'
        )
        input_area.add_widget(self.input)

        send_btn = Button(
            text="🦂 GÖNDER", size_hint_x=None, width=190,
            background_color=get_color_from_hex("#3897f0"), bold=True
        )
        send_btn.bind(on_release=self.send_message)
        input_area.add_widget(send_btn)
        self.root.add_widget(input_area)

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try: self.soc.bind(('', 9999))
        except: pass
        threading.Thread(target=self.receive_loop, daemon=True).start()
        return self.root

    def update_rect(self, *args):
        self.bg.pos = self.root.pos
        self.bg.size = self.root.size

    def send_message(self, instance):
        msg = self.input.text.strip()
        if msg:
            self.soc.sendto(f"{self.my_id}|{msg}".encode('utf-8'), ('255.255.255.255', 9999))
            self.add_bubble(msg, "right")
            self.input.text = ""

    def add_bubble(self, text, side):
        bg_color = (0.15, 0.8, 0.4, 0.95) if side == "right" else (0.2, 0.2, 0.2, 0.95)
        box = BoxLayout(size_hint_y=None, height=110)
        if side == "right": box.add_widget(Label(size_hint_x=0.25))
        bubble = Label(text=text, size_hint=(0.75, 1), markup=True, font_size='19sp')
        with bubble.canvas.before:
            Color(*bg_color)
            radius = [20, 20, 5, 20] if side == "right" else [20, 20, 20, 5]
            RoundedRectangle(pos=bubble.pos, size=bubble.size, radius=radius)
        box.add_widget(bubble)
        if side == "left": box.add_widget(Label(size_hint_x=0.25))
        self.chat_logs.add_widget(box)
        self.scroll.scroll_y = 0

    def receive_loop(self):
        while True:
            try:
                data, addr = self.soc.recvfrom(1024)
                decoded = data.decode('utf-8')
                if "|" in decoded:
                    sender_id, msg_content = decoded.split("|", 1)
                    if sender_id != self.my_id:
                        Clock.schedule_once(lambda dt: self.add_bubble(msg_content, "left"))
            except: pass

if __name__ == '__main__':
    AkrepVipGold().run()
