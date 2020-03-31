from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens import *


class MyApp(App):
    def build(self):
        self.title = "Rush Hour"
        sm = ScreenManager()
        sm.add_widget(MenuScreen())
        sm.add_widget(GameScreen())
        sm.add_widget(LevelsMenuScreen())
        sm.add_widget(InstructionsScreen())
        return sm


if __name__ == '__main__':
    MyApp().run()
