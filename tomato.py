import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, StringProperty
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

def on_enter(instance, value):
    print ('User pressed enter in', instance)

def on_text(instance, value):
    print ('User enter text:', value, 'in', instance)    

class TomatoPlayer(Widget):
    h = NumericProperty(0)
    m = NumericProperty(25)
    s = NumericProperty(0)
    time_strprop = StringProperty()
    goal_input = ObjectProperty(None)
    goal = StringProperty()
    start = BooleanProperty()

    def get_time_str(self):
        h_str = "00"
        m_str = str(self.m) if self.m >= 10 else "0"+str(self.m)
        s_str = str(self.s) if self.s >= 10 else "0"+str(self.s)
        return ":".join([h_str, m_str, s_str])

    def get_goal(self, textinput):
        self.goal = textinput.text
        textinput.text = ""
        self.remove_widget(self.goal_input)
        self.start = True
        
    def init_task(self):
        self.time_strprop = "00:25:00"
        self.start = False
        self.goal_input.bind(on_text_validate=self.get_goal)

    def update(self, t):
        if self.start:
            self.s -= 1
            if self.s == -1:
                self.s = 59
                self.m -= 1
            self.time_strprop = self.get_time_str()
        

class TomatoApp(App):
    def build(self):
        tomato = TomatoPlayer()
        tomato.init_task()
        Clock.schedule_interval(tomato.update, 1.0 / 10)
        return tomato

if __name__ == "__main__":
    TomatoApp().run()