from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget


class QRCodeApp(App):
    def build(self):
        return GUI


if __name__ == '__main__':
    GUI = Builder.load_file("QRCode.kv")
    QRCodeApp().run()
