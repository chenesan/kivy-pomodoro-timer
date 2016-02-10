from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.vector import Vector
from kivy.clock import Clock



class TomatoPlayer(Widget):
    h = StringProperty("00")
    m = StringProperty("25")
    s = StringProperty("00")
    def init_task(self):
        pass

    def update(self, t):
        pass

class TomatoApp(App):
    def build(self):
        tomato = TomatoPlayer()
        tomato.init_task()
        Clock.schedule_interval(tomato.update, 1.0 / 60.0)
        return tomato

if __name__ == "__main__":
    TomatoApp().run()