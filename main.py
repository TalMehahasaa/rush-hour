from kivy.app import App
from kivy.lang import Builder

kv = Builder.load_file("my.kv")


class MyApp(App):

    def build(self):
        self.title = "Rush Hour"
        return kv


if __name__ == '__main__':
    MyApp().run()
